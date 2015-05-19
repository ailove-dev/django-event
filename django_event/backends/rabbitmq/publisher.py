# -*- coding: utf-8 -*-

"""
RabbitMQ publisher module.
Contains asynchronous publisher for tornado and also blocking publisher for
django.
"""


from __future__ import unicode_literals

import json

from pika import BasicProperties
from pika import ConnectionParameters
from pika import PlainCredentials
from pika.adapters import BlockingConnection

from django_event.backends.base.publisher import BasePublisher
from django_event.backends.rabbitmq.client import RabbitMQClient


class Publisher(BasePublisher, RabbitMQClient):
    """
    Publisher class. Asynchronous by default.
    """

    def publish_message(self, message, channel='', *args, **kwargs):
        """
        Sends given message with specified content type and routing key.

        :param message: Message.
        :type message: serializable object

        :param channel: Routing key, see RabbitMQ docs for more info.
        :type channel: :class:`str`

        :param content_type: Message content type. Unusable for this backend.
        :type content_type: :class:`str`
        """

        if not self.channel:
            return

        content_type = kwargs.pop('content_type', 'application/json')

        message_json = json.dumps(message)

        properties = BasicProperties(content_type=content_type,
                                     delivery_mode=2)
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=channel,
                                   body=message_json,
                                   properties=properties)


class BlockingPublisher(Publisher):
    """
    Synchronous publisher class. Use it with django.
    """

    def connect(self):
        """
        Synchronous connection. Connects to RabbitMQ server and establish
        blocking connection. After connection is established call on_connected
        callback which will try to reconnect if this function failed.
        """

        if self.connecting and not self.reconnecting:
            return

        self.connecting = True
        credentials = PlainCredentials(self.username, self.password)
        param = ConnectionParameters(host=self.host,
                                     port=self.port,
                                     virtual_host=self.virtual_host,
                                     credentials=credentials)

        connection = BlockingConnection(param)
        self.on_connected(connection)

    def on_connected(self, connection):
        """
        Callback on connection. Reconnect if connection dropped. Otherwise it
        will open channel and call on_channel_open callback.

        :param connection: RabbitMQ connection.
        :type connection: :class:`BlockingConnection`
        """

        self.connection = connection
        if not self.connection:
            self.reconnecting = True
            self.reconnect()
        channel = self.connection.channel()
        self.on_channel_open(channel)

    def on_channel_open(self, channel):
        """
        Callback on channel open. It will declare exchanges for messaging. See
        RabbitMQ docs for more information.

        :param channel: Opened channel.
        :return: :class:`BlockingChannel`
        """

        self.channel = channel
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      type=self.exchange_type,
                                      auto_delete=False,
                                      durable=True)
