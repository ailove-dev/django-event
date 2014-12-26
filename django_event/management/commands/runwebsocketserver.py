# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from sockjs.tornado import SockJSRouter
from tornado.web import Application
from tornado.ioloop import IOLoop

from django_event import settings
from django_event.subscriber.connection import EventConnection


class Command(BaseCommand):
    """
    Django command to start tornado server.
    """

    def handle(self, *args, **options):
        host = settings.HOST
        port = settings.PORT

        router = SockJSRouter(EventConnection, host)
        app = Application(router.urls)
        app.listen(port)
        IOLoop.instance().start()