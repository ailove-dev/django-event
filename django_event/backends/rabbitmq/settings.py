# -*- coding: utf-8 -*-

"""
RabbitMQ backend specific settings module.
"""


from __future__ import unicode_literals

from django_event.backends.base.settings import *

HOST = HOST or 5672
VIRTUAL_HOST = settings.BACKEND_OPTIONS.get('VIRTUAL_HOST', '')
USERNAME = settings.BACKEND_OPTIONS.get('USERNAME', '')
QUEUE_NAME = settings.BACKEND_OPTIONS.get('QUEUE_NAME', 'default')