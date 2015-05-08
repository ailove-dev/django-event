# -*- coding: utf-8 -*-

"""
    Backend base client module.
"""

from __future__ import unicode_literals


class BaseClient(object):

    """
        Base backend client.
    """

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError