# -*- coding: utf-8 -*-

"""
Base Redis client module.
You basically don't need to use this module.
"""


from __future__ import unicode_literals

from django.conf import ImproperlyConfigured
from django_event.backends.base.client import BaseClient
from django_event.backends.redis import settings


class RedisClient(BaseClient):
    """
    Base Redis adapter.
    """

    def __init__(self,
                 host=settings.HOST,
                 port=settings.PORT,
                 db=settings.DB,
                 password=settings.PASSWORD,
                 use_redis_cache=settings.USE_REDIS_CACHE,
                 socket_connect_timeout=settings.SOCKET_CONNECT_TIMEOUT,
                 socket_timeout=settings.SOCKET_TIMEOUT,
                 unix_socket_path=settings.UNIX_SOCKET_PATH):
        """
        Initialize Redis client with passed configuration or get parameters
        from django settings module.

        :param host: Redis host
        :type host: :class:`str`

        :param port: Redis port
        :type port: :class:`int`

        :param port: Redis db
        :type port: :class:`int`

        :param password: Redis password
        :type password: :class:`str`

        :param use_redis_cache: Use django_redis configured connection
        :type use_redis_cache: :class:`bool`

        :param socket_connect_timeout: Socket connect timeout
        :type socket_connect_timeout: :class:`int`

        :param socket_timeout: Socket timeout
        :type socket_timeout: :class:`int`

        :param unix_socket_path: If passed unix socket connection will be
         established instead of http
        :type unix_socket_path: :class:`str`
        """

        self.use_redis_cache = use_redis_cache

        if not use_redis_cache:
            self.client_kwargs = {
                'host': host,
                'port': int(port),
                'password': password,
                'db': db,
                'socket_connect_timeout': socket_connect_timeout,
                'socket_timeout': socket_timeout,
                'unix_socket_path': unix_socket_path,
            }

        self.client = None
        self.pub_sub_client = None

    def connect(self):
        """
        Connects to Redis server and establish connection.
        """

        if self.use_redis_cache:
            from django_redis import get_redis_connection

            self.client = get_redis_connection(self.use_redis_cache)
        else:
            from redis import StrictRedis

            self.client = StrictRedis(**self.client_kwargs)

        self.pub_sub_client = self.client.pubsub(ignore_subscribe_messages=True)

    def disconnect(self):
        """
        Don't need to manually disconnect this backend.
        """

        pass
