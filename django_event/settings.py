# -*- coding: utf-8 -*-

"""

Available django-event settings:

.. literalinclude:: ../django_event/settings.py
    :lines: 14-

"""

from __future__ import unicode_literals

from django.conf import settings


event_settings = settings.DJANGO_EVENT


BACKEND = event_settings.get('BACKEND', 'rabbitmq')

BACKEND_HOST = event_settings.get('BACKEND_HOST', 'localhost')
BACKEND_PORT = event_settings.get('BACKEND_PORT')
BACKEND_VIRTUALHOST = event_settings.get('BACKEND_VIRTUALHOST', '')
BACKEND_USERNAME = event_settings.get('BACKEND_USERNAME', '')
BACKEND_PASSWORD = event_settings.get('BACKEND_PASSWORD', '')
BACKEND_QUEUENAME = event_settings.get('BACKEND_QUEUENAME', 'default')
BACKEND_CACHE = event_settings.get('BACKEND_CACHE')


TORNADO_HOST = event_settings.get('TORNADO_HOST', '/')
TORNADO_PORT = event_settings.get('TORNADO_PORT', 8989)

LISTENER_CLASSES = event_settings.get('EVENT_LISTENER_CLASSES', {})

EVENT_STORE_DAYS = event_settings.get('EVENT_STORE_DAYS', 7)