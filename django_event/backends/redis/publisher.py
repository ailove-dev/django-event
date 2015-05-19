# -*- coding: utf-8 -*-

"""
Redis publisher module.
Contains asynchronous publisher for tornado and also blocking publisher for
django.
"""


from __future__ import unicode_literals

import json
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop

from django_event.backends.base.publisher import BasePublisher
from django_event.backends.redis.client import RedisClient


class BlockingPublisher(BasePublisher, RedisClient):
    """
    Synchronous publisher class. Use it with django.
    """

    def publish_message(self, message, channel=None, *args, **kwargs):
        """
        Sends given message with routing key.

        :param message: Message.
        :type message: serializable object

        :param channel: Redis channel.
        :type channel: :class:`str`
        """

        self._publish_message(message, channel=channel)

    def _publish_message(self, message, channel=''):
        """
        Sends given message with routing key.

        :param message: Message.
        :type message: serializable object

        :param channel: Redis channel.
        :type channel: :class:`str`
        """

        if not self.client:
            return

        message_json = json.dumps(message)

        self.client.publish(channel, message_json)


class Publisher(BlockingPublisher):
    """
    Publisher class. Asynchronous.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize publisher.
        """

        super(Publisher, self).__init__(*args, **kwargs)

        self.io_loop = IOLoop.instance()
        self.executor = ThreadPoolExecutor(max_workers=cpu_count())

    @run_on_executor
    def publish_message(self, message, channel='', *args, **kwargs):
        """
        Sends given message with routing key.

        :param message: Message.
        :type message: serializable object

        :param channel: Redis channel.
        :type channel: :class:`str`
        """

        self._publish_message(message, channel=channel)
