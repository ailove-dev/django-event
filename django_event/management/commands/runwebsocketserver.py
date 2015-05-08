# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from sockjs.tornado import SockJSRouter
from tornado.web import Application
from tornado.ioloop import IOLoop

from django_event.management.commands import settings
from django_event.subscriber.connection import EventConnection


class Command(BaseCommand):
    """
    Django command to start tornado server.
    """

    def handle(self, *args, **options):
        router = SockJSRouter(EventConnection, settings.HOST)
        app = Application(router.urls)
        app.listen(settings.PORT)

        try:
            IOLoop.instance().start()
        except KeyboardInterrupt:
            pass