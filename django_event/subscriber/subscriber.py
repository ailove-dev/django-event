# -*- coding: utf-8 -*-

"""
RabbitMQ subscribes module.
Contains asynchronous publisher for tornado.
"""


import types

from django_event.utils import import_var
from django_event.subscriber.listeners import Listener
from django_event.rabbitmq.client import RabbitMQClient


class Subscriber(RabbitMQClient):
    """
    Base subscriber class. Asynchronous by default.
    """

    def __init__(self,
                 queue_name='',
                 routing_key='',
                 *args, **kwargs):
        """
        Initialize RabbitMQ client with passed configuration or get parameters
        from django settings module plus subscribes-specific arguments.

        :param queue_name: RabbitMQ queue name, see RabbitMQ docs for more info.
        :type queue_name: :class:`str`

        :param routing_key: RabbitMQ routing key, see RabbitMQ docs for more
         info.
        :type routing_key: :class:`str`

        :param args: RabbitMQ client init args.

        :param kwargs: RabbitMQ client init kwargs.
        """

        super(Subscriber, self).__init__(*args, **kwargs)

        self.queue_name = queue_name
        self.routing_key = routing_key

        self.event_listeners = set([])

    ############################################################################
    # CALLBACKS
    ############################################################################

    def on_channel_open(self, channel):
        """
        Callback on channel open. Overrides base method for setting callback.
        on_exchange_declared callback will be executed internally.

        :param channel: Opened channel.
        :type channel: :class:`Channel`
        """

        super(Subscriber, self).on_channel_open(
            channel, callback=self.on_exchange_declared)

    def on_exchange_declared(self, frame):
        """
        Callback on exchange declared. Declare queue.
        on_queue_declared callback will be executed internally.

        :param frame: Frame instance.
        :type frame: Frame
        """

        # TODO: add queue name

        self.channel.queue_declare(exclusive=True,
                                   durable=True,
                                   auto_delete=False,
                                   callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        """
        Callback on queue declared. Bind queue.
        on_queue_bind callback will be executed internally.

        :param frame: Frame instance.
        :type frame: Frame
        """

        self.queue_name = frame.method.queue
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue=self.queue_name,
                                routing_key=self.routing_key,
                                callback=self.on_queue_bind)

    def on_queue_bind(self, frame):
        """
        Callback on queue bound. Starts consume messages.
        on_message callback will be executed internally.

        :param frame: Frame instance.
        :type frame: Frame
        """

        self.channel.basic_consume(self.on_message,
                                   queue=self.queue_name,
                                   no_ack=True)

    def on_message(self, channel, method, header, body):
        """
        Callback. Called internally. Notifies all listeners about consumed
        message. Called internally by on_queue_bind on message consumed.

        :param channel: Opened channel.
        :type channel: :class:`Channel`

        :param method: Method.
        :type method: Method

        :param header: Message's headers.
        :type header: :class:`str`

        :param body: Consumed message's body.
        :type body: :class:`str`
        """

        for listener in self.event_listeners:
            listener.on_message(body)

    ############################################################################
    # LISTENER METHODS
    ############################################################################

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

