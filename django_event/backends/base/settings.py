# -*- coding: utf-8 -*-

"""
Base backend specific settings module.
"""


from __future__ import unicode_literals

from django_event import settings


HOST = settings.BACKEND_OPTIONS.get('HOST', 'localhost')
PORT = settings.BACKEND_OPTIONS.get('PORT', 5672)
PASSWORD = settings.BACKEND_OPTIONS.get('PASSWORD', '')