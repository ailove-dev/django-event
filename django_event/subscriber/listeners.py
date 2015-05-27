# -*- coding: utf-8 -*-

"""
Base listener module.
"""


from __future__ import unicode_literals

import json
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from django.utils.lru_cache import lru_cache
from tornado.ioloop import IOLoop
from tornado.concurrent import run_on_executor

from django_event import settings
from django_event.utils import get_routing
from django_event.utils import import_var


class Listener(object):
    """
    Abstract base listener class. Listeners used by subscribers.
    """

    executor = ThreadPoolExecutor(max_workers=cpu_count())
    io_loop = IOLoop.current()

    def __init__(self, user):
        """
        Initialize listener.

        :param user: Django user instance
        :type user: User
        """

        self._user = user
        self._routing_key = None
        self._message = None

    def __eq__(self, other):
        if not isinstance(other, Listener):
            return False
        return (
            self._user == other._user and
            self._routing_key == other._routing_key
        )

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    @run_on_executor
    @lru_cache()
    def get_listener(cls, event_type):
        """
        Fabric method for listener subclasses.
        Imports listener by type and returns it.

        :param event_type: Event type.
        :type event_type: :class:`str`

        :return: Listener module that will process certain type of messages.
        :rtype: :class:`Listener` subclass
        """

        return import_var(settings.LISTENERS[event_type])

    def on_message(self, message):
        """
        Abstract method. Specifies on message behaviour.

        :param message: Received message.
        :type message: :class:`str`

        :raise: NotImplementedError
        """

        raise NotImplementedError

    def routing_matched(self):
        """
        Computes routing key for current user and compares with received
        message's routing key.

        :return: True if routing key matched.
        :rtype: :class:`bool`
        """

        self._routing_key = get_routing(self._user,
                                        self._message['routing_strategy'])
        return self._routing_key == self._message['routing_key']


class SendMessageListener(Listener):
    """
    Base listener for send message through SockJS connection.
    """

    def __init__(self, user, sender):
        """
        Initialize listener.

        :param user: Django user instance.
        :type user: User

        :param sender: Send function
        :type sender: callable object
        """

        super(SendMessageListener, self).__init__(user)

        self.sender = sender

    def on_message(self, message):
        """
        Sends message if routing key matched.

        :param message: Received message.
        :type message: :class:`str`
        """

        self._message = json.loads(message)
        if self.routing_matched():
            self.sender(json.dumps(self._message['message']))