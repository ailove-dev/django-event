# -*- coding: utf-8 -*-

"""
Core event server module.
Provides basic websocket connection and subscribe/unsubscribe message system.
"""


from __future__ import unicode_literals

import json
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from django import db
from django.conf import settings
from django.contrib.auth import get_user as _get_user
from django.contrib.sessions.exceptions import InvalidSessionKey
from django.utils.importlib import import_module
from sockjs.tornado.conn import SockJSConnection
from tornado import gen
from tornado.concurrent import run_on_executor

from django_event.backends import Backend
from django_event.subscriber.listeners import Listener


_engine = import_module(settings.SESSION_ENGINE)


class _Request(object):
    """
    Private class that emulates Django Request class.
    """

    pass


def get_session(session_key):
    """
    Returns Django session instance by session key.

    :param session_key: Session key given through websocket.
    :type session_key: :class:`str`

    :return: Session.
    :rtype: Django session
    """

    return _engine.SessionStore(session_key)


def get_user(session):
    """
    Returns Django User instance by session.

    :param session: User's session.
    :type session: Django session

    :return: User.
    :rtype: Django User
    """

    django_request = _Request()
    django_request.session = session

    return _get_user(django_request)


class EventConnection(SockJSConnection):
    """
    SockJS connection handler.
    """

    # Thread pool for synchronous methods.
    executor = ThreadPoolExecutor(max_workers=cpu_count())

    def __init__(self, session):
        """
        Initialize connection.

        :param session: Session passed on initializing connection.
        :type session: Django session
        """

        super(EventConnection, self).__init__(session)

        self.subscribers = {}
        self.user = None

    @gen.coroutine
    def on_open(self, request):
        """
        Asynchronous callback. Basic authentication by session implemented.
        Called internally by base class on connection opened.

        :param request: Request given on connection open.
        :type request: Tornado Request
        """

        try:
            self.user = yield self.authenticate(request)
        except (db.Error, InvalidSessionKey):
            self.close()

    @run_on_executor
    def authenticate(self, request):
        """
        Authenticates user by session key.

        :param request: Request given on connection open.
        :type request: Tornado Request

        :return: Authenticated user.
        :rtype: Django User
        """

        user = get_user(get_session(request.get_cookie('sessionid').value))

        if not user:
            raise InvalidSessionKey('Session id was not provided')

        return user

    @gen.coroutine
    def on_message(self, message):
        """
        Asynchronous callback.
        Called internally by base class on message received.
        Provides message routing. Subscribes and unsubscribes on messages types.

        :param message: JSON message received from RabbitMQ.
        :type message: :class:`str`
        """

        if not self.user:
            return

        actions = {
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe
        }

        message = json.loads(message)
        message_type = message.get('type')

        actions.get(message_type, self.wrong_message)(message)

    @gen.coroutine
    def subscribe(self, message):
        """
        Subscribes event listeners on messages.

        :param message: JSON decoded message routed by on_message method.
        :type message: :class:`dict`
        """

        subscribe_list = message.get('args', [])
        for subject in subscribe_list:
            if subject not in self.subscribers:
                self.subscribers[subject] = Backend.subscriber(channel=subject)
                listener = yield Listener.get_listener(subject)
                self.subscribers[subject].add_event_listener(
                    listener,
                    self.user,
                    self.send
                )
                self.subscribers[subject].connect()

    @gen.coroutine
    def wrong_message(self, message):
        """
        Overridable method for wrong message type.

        :param message: JSON decoded message routed by on_message method.
        :type message: :class:`dict`
        """

        pass

    @gen.coroutine
    def unsubscribe(self, message):
        """
        Unsubscribes event listeners from messages.

        :param message: JSON decoded message routed by on_message method.
        :type message: :class:`dict`
        """

        subscribe_list = message.get('args', [])
        for subject in subscribe_list:
            if subject in self.subscribers:
                subscriber = self.subscribers.pop(subject)
                subscriber.disconnect()
                listener = yield Listener.get_listener(subject)
                subscriber.remove_event_listener(listener)

    @gen.coroutine
    def send(self, message, binary=False):
        """
        Sends message to websocket.

        :param message: JSON decoded message routed by on_message method.
        :type message: :class:`dict`

        :param binary: Flag. True if message need to be send in binary.
        :type binary: :class:`bool`
        """

        super(EventConnection, self).send(message, binary)

    @gen.coroutine
    def on_close(self):
        """
        Asynchronous callback.
        Called internally by base class on connection closed.
        Unsubscribes all event listeners.
        """

        for subscriber in self.subscribers.itervalues():
            subscriber.disconnect()
