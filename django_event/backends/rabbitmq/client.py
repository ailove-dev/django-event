# -*- coding: utf-8 -*-

"""
Base RabbitMQ client module.
You basically don't need to use this module.
"""


from __future__ import unicode_literals

from pika import ConnectionParameters
from pika import PlainCredentials
from pika.adapters import TornadoConnection

from django_event.backends.base.client import BaseClient
from django_event.backends.rabbitmq import settings


class RabbitMQClient(BaseClient):
    """
    Base RabbitMQ asynchronous adapter.
    """

    def __init__(self,
                 host=settings.HOST,
                 port=settings.PORT,
                 virtual_host=settings.VIRTUAL_HOST,
                 username=settings.USERNAME,
                 password=settings.PASSWORD,
                 exchange_name='direct',
                 exchange_type='direct'):
        """
        Initialize RabbitMQ client with passed configuration or get parameters
        from django settings module.

        :param host: RabbitMQ host
        :type host: :class:`str`

        :param port: RabbitMQ port
        :type port: :class:`int`

        :param virtual_host: RabbitMQ virtual host
        :type virtual_host: :class:`str`

        :param username: RabbitMQ user
        :type username: :class:`str`

        :param password: RabbitMQ user's password
        :type password: :class:`str`

        :param exchange_name: Exchange name, see RabbitMQ docs for more info.
        :type exchange_name: :class:`str`

        :param exchange_type: Exchange type, see RabbitMQ docs for more info.
        :type exchange_type: :class:`str`
        """

        self.host = host
        self.port = int(port)
        self.virtual_host = virtual_host
        self.username = username
        self.password = password
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type

        self.connected = False
        self.connecting = False
        self.reconnecting = False
        self.closing = False

        self.connection = None
        self.channel = None

    ############################################################################
    # CONNECTION METHODS
    ############################################################################

    def connect(self):
        """
        Asynchronous connection. Connects to RabbitMQ server and establish
        non-blocking connection. After connection is established on_connected
        callback will be executed which will try to reconnect if this function
        failed.
        """

        if self.connecting and not self.reconnecting:
            return

        self.connecting = True
        credentials = PlainCredentials(self.username, self.password)
        param = ConnectionParameters(host=self.host,
                                     port=self.port,
                                     virtual_host=self.virtual_host,
                                     credentials=credentials)

        self.connection = TornadoConnection(param,
                                            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_close)

    def reconnect(self):
        """
        Reconnect method.
        Basically you don't need to call this method manually.
        """

        self.reconnecting = True
        self.connect()

    def disconnect(self):
        """
        Disconnect method.
        Call this method after you end with messaging.
        """

        self.closing = True
        self.connection.close()

    ############################################################################
    # CALLBACKS
    ############################################################################

    def on_connected(self, connection):
        """
        Callback on connection. Reconnect if connection dropped. Otherwise it
        will open channel and on_channel_open callback will be executed.

        :param connection: RabbitMQ connection.
        :type connection: :class:`TornadoConnection`
        """

        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel, callback=lambda frame: None):
        """
        Callback on channel open. It will declare exchanges for messaging. See
        RabbitMQ docs for more information.

        :param channel: Opened channel.
        :type channel: :class:`Channel`

        :param callback: Callback that will be executed after channel open.
        :type callback: callable object
        """

        self.channel = channel
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      type=self.exchange_type,
                                      auto_delete=False,
                                      durable=True,
                                      callback=callback)

    def on_close(self, connection, *args, **kwargs):
        """
        On close callback.
        You don't need to manually call this method.

        :param connection: Established connection.
        :type connection: :class:`TornadoConnection`

        :param args: Internal args
        :param kwargs: Internal kwargs
        """

        self.channel = None
        if not self.closing:
            self.reconnect()
            self.connection.add_timeout(5, self.reconnect)
        else:
            connection.close()
