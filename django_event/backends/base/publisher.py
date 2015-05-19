# -*- coding: utf-8 -*-

"""
Backend base subscribed module.
"""

from __future__ import unicode_literals


class BasePublisher(object):

    def __init__(self, *args, **kwargs):
        """
        Initialize publisher.
        """

        super(BasePublisher, self).__init__(*args, **kwargs)

    def publish_message(self, message, channel=None, *args, **kwargs):
        """
        Publish message abstract method.

        :param message: Message body
        :type message: :class:`str`

        :param channel: Channel
        :type channel: :class:`str`

        :raises: :class:`NotImplementedError`
        """

        raise NotImplementedError
