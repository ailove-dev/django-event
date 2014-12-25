# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand
from sockjs.tornado import SockJSRouter
from tornado.web import Application
from tornado.ioloop import IOLoop

from ...subscriber.connection import EventConnection


class Command(BaseCommand):
    """
    Django command to start tornado server.
    """

    def handle(self, *args, **options):
        host = getattr(settings, 'EVENT_HOST', '/')
        port = getattr(settings, 'EVENT_PORT', 8989)

        router = SockJSRouter(EventConnection, host)
        app = Application(router.urls)
        app.listen(port)
        IOLoop.instance().start()