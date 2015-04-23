# -*- coding: utf-8 -*-

"""
Serializers module for django rest_framework.
"""

from __future__ import unicode_literals

from django.utils import timezone
from rest_framework import serializers

from django_event.models import Event


class LocalDateTimeField(serializers.DateTimeField):
    """
    Automatically converts server time into local time.
    """

    def to_representation(self, value):
        """
        Converts UTC to local time.

        :param value: UTC datetime from db.
        :type value: :class:`DateTime`
        """
        return super(LocalDateTimeField, self).to_representation(
            value if value is None else timezone.localtime(value)
        )


class EventSerializer(serializers.ModelSerializer):
    """
    Specifies which fields should be serialized and overrides date fields to
    return local time instead of server time.
    """

    created_at = LocalDateTimeField()
    started_at = LocalDateTimeField()
    completed_at = LocalDateTimeField()

    class Meta:
        model = Event