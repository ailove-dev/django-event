# -*- coding: utf-8 -*-

"""
    Backend selector module.
"""

from __future__ import unicode_literals

from django.conf import ImproperlyConfigured
from django.utils.functional import cached_property

from django_event.settings import BACKEND
from django_event.utils import import_var


class BackendSelector(object):
    RABBITMQ = 'rabbitmq'
    REDIS = 'redis'

    AVAILABLE_BACKENDS = (
        RABBITMQ,
        REDIS,
    )

    @classmethod
    @property
    def valid_backend_setting(cls):
        """
        Checks if configured backed is valid.

        :return: True if valid, False otherwise.
        :rtype: :class:`bool`
        """

        return BACKEND in cls.AVAILABLE_BACKENDS

    @cached_property
    def backends(self):
        """
        Selects event backend. If backend is unavailable raises
        ImproperlyConfigured exception. The first item in returned tuple is
        :class:`Publisher` class, second is :class:`BlockingPublisher` and
        third is :class:`Subscriber`

        :return: :class:`Publisher`, :class:`BlockingPublisher`,
         :class:`Subscriber` classes

        :raise ImproperlyConfigured:
        """

        if not self.valid_backend_setting:
            raise ImproperlyConfigured(
                'Invalid backend setting. Available backends are %s' %
                str(self.AVAILABLE_BACKENDS)
            )
        publisher = import_var(
            'django_event.backends.%s.publisher.Publisher' % BACKEND
        )
        blocking_publisher = import_var(
            'django_event.backends.%s.publisher.BlockingPublisher' % BACKEND
        )
        subscriber = import_var(
            'django_event.backends.%s.subscriber.Subscriber' % BACKEND
        )

        return publisher, blocking_publisher, subscriber

    @property
    def publisher(self):
        """

        Property to publisher class.

        :return: Publisher class.
        """

        return self.backends[0]

    @property
    def blocking_publisher(self):
        """

        Property to blocking publisher class.

        :return: BlockingPublisher class.
        """

        return self.backends[1]

    @property
    def subscriber(self):
        """

        Property to subscriber class.

        :return: Subscriber class.
        """

        return self.backends[2]