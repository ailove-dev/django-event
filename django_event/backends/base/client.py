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
        """
        Establishes connection.

        :raises: :class:`NotImplementedError`
        """

        raise NotImplementedError

    def disconnect(self):
        """
        Disconnects.

        :raises: :class:`NotImplementedError`
        """

        raise NotImplementedError