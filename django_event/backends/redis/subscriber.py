# -*- coding: utf-8 -*-

"""
Redis subscribers module.
Contains asynchronous publisher for tornado.
"""


from __future__ import unicode_literals

import time
from multiprocessing import cpu_count

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop

from django_event.backends.base.subscriber import BaseSubscriber
from django_event.backends.redis.client import RedisClient


class Subscriber(BaseSubscriber, RedisClient):
    """
    Base subscriber class. Asynchronous by default.
    """

    def __init__(self, channel='', *args, **kwargs):
        """
        Initialize subscriber.

        :param channel: Redis channel.
        :type channel: :class:`str`
        """

        super(Subscriber, self).__init__(*args, **kwargs)

        self.channel = channel
        self._consume = True
        self.io_loop = IOLoop.current()
        self.executor = ThreadPoolExecutor(max_workers=cpu_count())

    @run_on_executor
    def consume(self):
        """
        Consumes messages in separate thread and notifies event listeners.
        """

        message = self.pub_sub_client.get_message()
        if message:
            self.notify_listeners(message['data'])
        if self._consume:
            self.io_loop.add_callback(self.consume)
        time.sleep(0.01)

    def connect(self):
        """
        Connects to Redis server and establish connection. Starts consume
        messages.
        """

        super(Subscriber, self).connect()
        self.pub_sub_client.subscribe(self.channel)
        self.consume()

    def disconnect(self):
        """
        Sets consume flag to false to stop consuming messages.
        """

        self._consume = False