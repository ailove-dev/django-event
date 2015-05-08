# -*- coding: utf-8 -*-

"""
    Backend base publisher module.
"""

from __future__ import unicode_literals

import types

from django_event.utils import import_var
from django_event.subscriber.listeners import Listener


class BaseSubscriber(object):

    def __init__(self):
        self.event_listeners = set([])

    @staticmethod
    def _import_listener(listener):
        """
        Imports listener class.

        :param listener: Listener class to import
        :type listener: :class:`str`

        :return: Listener class
        :rtype: :class:`Listener` subclass

        :raise: :class:`AttributeError` if listener doesn't have on_message
         method.
        """

        listener_class = import_var(listener)

        if (not hasattr(listener_class, 'on_message') or
                not callable(listener_class.on_message)):
            raise AttributeError(
                'Listener %s doesnt have on_message(message) method' % listener)

        return listener_class

    def add_event_listener(self, listener, *args, **kwargs):
        """
        Adds event listener for dispatch messages.
        Raises Exception if got listener of unexpected type.

        :param listener: Message listener
        :type listener: :class:`str` or :class:`Listener` subclass or
         :class:`Listener` instance

        :param args: :class:`Listener` init args
        :param kwargs: :class:`Listener` init kwargs

        :raise: :class:`TypeError` if listeners of unknown type passed into.
        """

        if isinstance(listener, str):
            self.event_listeners.add(
                self._import_listener(listener)(*args, **kwargs))
        elif issubclass(listener, Listener):
            self.event_listeners.add(listener(*args, **kwargs))
        elif isinstance(listener, Listener):
            self.event_listeners.add(listener)
        else:
            raise TypeError('Wrong listener type')

    def remove_event_listener(self, listener):
        """
        Remove event listener.

        :param listener: Message listener
        :type listener: :class:`str` or :class:`Listener` subclass or
         :class:`Listener` instance

        :raise: :class:`KeyError` if listener not found.
        :raise: :class:`TypeError' if listener has wrong type.
        """

        if isinstance(listener, Listener):
            self.event_listeners.remove(listener)
        elif isinstance(listener, types.ClassType):
            for listener_in in self.event_listeners:
                if isinstance(listener_in, listener):
                    self.event_listeners.remove(listener_in)
        elif isinstance(listener, str):
            listener = listener.split('.').pop()
            for listener_in in self.event_listeners:
                if listener == listener_in.__class__.__name__:
                    self.event_listeners.remove(listener_in)
        else:
            raise TypeError('Wrong listener type')

    def notify_listeners(self, message):
        """
        Notifies all listeners about consumed message.

        :param message: Consumed message's body.
        :type message: :class:`str`
        """

        for listener in self.event_listeners:
            listener.on_message(message)