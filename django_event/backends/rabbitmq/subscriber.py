# -*- coding: utf-8 -*-

"""
RabbitMQ subscribers module.
Contains asynchronous publisher for tornado.
"""


from __future__ import unicode_literals


from django_event.backends.base.subscriber import BaseSubscriber
from django_event.backends.rabbitmq import settings
from django_event.backends.rabbitmq.client import RabbitMQClient


class Subscriber(BaseSubscriber, RabbitMQClient):
    """
    Base subscriber class. Asynchronous by default.
    """

    def __init__(self,
                 queue_name=settings.QUEUE_NAME,
                 channel='',
                 *args, **kwargs):
        """
        Initialize RabbitMQ client with passed configuration or get parameters
        from django settings module plus subscribes-specific arguments.

        :param queue_name: RabbitMQ queue name, see RabbitMQ docs for more info.
        :type queue_name: :class:`str`

        :param channel: RabbitMQ routing key, see RabbitMQ docs for more
         info.
        :type channel: :class:`str`

        :param args: RabbitMQ client init args.

        :param kwargs: RabbitMQ client init kwargs.
        """

        super(Subscriber, self).__init__(*args, **kwargs)

        self.queue_name = queue_name
        self.routing_key = channel

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

        self.channel.queue_declare(exclusive=False,
                                   durable=True,
                                   auto_delete=True,
                                   queue=self.queue_name,
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

        self.notify_listeners(body)

