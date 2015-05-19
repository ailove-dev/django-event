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
BACKEND_OPTIONS = event_settings.get('BACKEND_OPTIONS', {})

TORNADO_OPTIONS = event_settings.get('TORNADO_OPTIONS', {})

LISTENERS = event_settings.get('LISTENERS', {})

STORE_DAYS = event_settings.get('STORE_DAYS', 7)

EVENT_MODEL = event_settings.get('EVENT_MODEL', 'django_event.Event')

AVAILABLE_TYPES = [key for key in LISTENERS.iterkeys()]