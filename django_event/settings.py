# -*- coding: utf-8 -*-

"""

Available django-event settings:

.. literalinclude:: ../django_event/settings.py
    :lines: 14-

"""

from __future__ import unicode_literals

from django.conf import settings

################################################################################
# REQUIRED SETTINGS
################################################################################

RABBITMQ_HOST = settings.EVENT_RABBITMQ_HOST

RABBITMQ_PORT = settings.EVENT_RABBITMQ_PORT

RABBITMQ_VIRTUALHOST = settings.EVENT_RABBITMQ_VIRTUALHOST

RABBITMQ_USERNAME = settings.EVENT_RABBITMQ_USERNAME

RABBITMQ_PASSWORD = settings.EVENT_RABBITMQ_PASSWORD

LISTENER_CLASSES = settings.EVENT_LISTENER_CLASSES

################################################################################
# OPTIONAL SETTINGS
################################################################################

# HOST WHERE TORNADO SHOULD RUN SERVER
HOST = getattr(settings, 'EVENT_HOST', '/')

# TORNADO PORT
PORT = getattr(settings, 'EVENT_PORT', 8989)

# HOW LONG STORE EVENTS
STORE_DAY = getattr(settings, 'EVENT_STORE_DAY', 7)