# -*- coding: utf-8 -*-

"""
Exceptions module.
"""

from __future__ import unicode_literals


class EventError(Exception):
    """Using to notify subscribed clients about event failure."""

    pass