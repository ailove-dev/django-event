# -*- coding: utf-8 -*-

"""
RabbitMQ backend specific settings module.
"""


from __future__ import unicode_literals

from django_event.backends.base.settings import *

HOST = HOST or 6379
DB = settings.BACKEND_OPTIONS.get('DB', 0)
USE_REDIS_CACHE = settings.BACKEND_OPTIONS.get('USE_REDIS_CACHE', False)
SOCKET_TIMEOUT = settings.BACKEND_OPTIONS.get('SOCKET_TIMEOUT')
SOCKET_CONNECT_TIMEOUT = settings.BACKEND_OPTIONS.get('SOCKET_CONNECT_TIMEOUT')
UNIX_SOCKET_PATH = settings.BACKEND_OPTIONS.get('UNIX_SOCKET_PATH')