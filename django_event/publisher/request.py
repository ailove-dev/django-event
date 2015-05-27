# -*- coding: utf-8 -*-

"""
Event request module.

Usage examples:
You can pass custom arguments into decorated function which are not required. ::

   EventRequest(django_request, custom_argument=123)

But django request is must for event. ::

   EventRequest(django_request)
"""


from __future__ import unicode_literals

import json


class _DummyUser:
    """
    Private class that emulates Django User class.
    """

    def __init__(self, user_id):
        """
        Only id needed.

        :param user_id: Django user id.
        :type user_id: :class:`int`
        """

        self.id = user_id


class _DummyRequest:
    """
    Private class that emulates Django Request class.
    """

    def __init__(self, data, user):
        """
        Only user and data needed.

        :param data: Django request data
        :type data: :class:`QueryDict`

        :param user: Django user
        :type user: :class:`User` or :class:`_DummyUser`
        """

        self.data = data
        self.user = user


class mutable(object):
    """
    Context manager for modifying django request.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.ctx_maybe_mutable = getattr(self.ctx, '_mutable', None)
        if self.ctx_maybe_mutable is None:
            self.ctx_immutable = False
        else:
            self.ctx_immutable = not self.ctx_maybe_mutable

    def __enter__(self):
        if self.ctx_immutable:
            self.ctx._mutable = not self.ctx._mutable
        return self.ctx

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ctx_immutable:
            self.ctx._mutable = not self.ctx._mutable


class EventRequest(object):
    """
    Event request class user to pass arguments to decorated events.

    """
    def __init__(self, django_request, **kwargs):
        """
        Copies django request data and set some internal arguments.

        :param django_request: Django request.
        :type django_request: :class:`Request` or :class:`_RequestDummy`

        :param kwargs: Custom arguments needed by task.
        """

        self.data = getattr(django_request, 'data', None)
        self.data = self.data or getattr(django_request, 'POST')
        self.user_id = django_request.user.id
        with mutable(self.data):
            self.send_mail = self.data.pop('send_mail', True)
        self.custom_args = kwargs

    def __getattr__(self, item):
        """
        Magick method for dot notation for custom task arguments.
        """

        try:
            return self.__getattribute__('custom_args')[item]
        except KeyError:
            raise AttributeError(item)

    def serialize(self):
        """
        Serialize event request into JSON for database storing.

        :return: JSON serialized event request.
        :rtype: :class:`str`
        """

        return json.dumps({
            'data': self.data,
            'user_id': self.user_id,
            'send_mail': self.send_mail,
            'custom_args': self.custom_args
        })

    @staticmethod
    def deserialize(json_request, return_dummy=False):
        """
        Deserialize JSON request and returns EventRequest instance or
        dict which contains Dummy classes.

        :param json_request: JSON serialized event request.
        :type json_request: :class:`str`

        :param return_dummy: Return EventRequest or dict with dummies.
        :type return_dummy: :class:`bool`

        :return: Deserialized instance.
        :rtype: :class:`EventRequest` or :class:`dict`
        """

        dict_request = json.loads(json_request)

        user = _DummyUser(dict_request['user_id'])
        request = _DummyRequest(dict_request['data'], user)

        if return_dummy:
            return request, dict_request['custom_args']

        return EventRequest(request, **dict_request['custom_args'])