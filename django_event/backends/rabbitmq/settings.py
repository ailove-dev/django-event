# -*- coding: utf-8 -*-

"""
RabbitMQ backend specific settings module.
"""


from __future__ import unicode_literals

from django_event import settings


HOST = settings.BACKEND_OPTIONS.get('HOST', 'localhost')
PORT = settings.BACKEND_OPTIONS.get('PORT', 5672)
VIRTUAL_HOST = settings.BACKEND_OPTIONS.get('VIRTUAL_HOST', '')
USERNAME = settings.BACKEND_OPTIONS.get('USERNAME', '')
PASSWORD = settings.BACKEND_OPTIONS.get('PASSWORD', '')
QUEUE_NAME = settings.BACKEND_OPTIONS.get('QUEUE_NAME', 'default')