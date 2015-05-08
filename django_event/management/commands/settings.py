# -*- coding: utf-8 -*-

"""
Tornado specific settings module.
"""


from __future__ import unicode_literals

from django_event import settings


HOST = settings.TORNADO_OPTIONS.get('HOST', '/')
PORT = settings.TORNADO_OPTIONS.get('PORT', 8989)