# -*- coding: utf-8 -*-

"""
    Backend base subscribed module.
"""

from __future__ import unicode_literals


class BasePublisher(object):

    def publish_message(self, *args, **kwargs):
        raise NotImplementedError