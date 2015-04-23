# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import NoArgsCommand

from django_event.models import Event


class Command(NoArgsCommand):
    """
    Django command to delete old events.
    """

    def handle_noargs(self, **options):
        Event.delete_old()
