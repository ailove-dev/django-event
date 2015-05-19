# -*- coding: utf-8 -*-

"""
Urls for django. ::

    urlpatterns = patterns(
        '',
        url(
            r'^$',
            event_list,
            name='event_list'
        ),
        url(
            r'^(?P<pk>[0-9]+)/$',
            event_detail,
            name='event_detail'
        ),
        url(
            r'^(?P<pk>[0-9]+)/cancel/$',
            cancel_event,
            name='cancel_event'
        ),
        url(
            r'^(?P<pk>[0-9]+)/retry/$',
            retry_event,
            name='retry_event'
        ),
    )

"""


from __future__ import unicode_literals

from django.conf.urls import patterns
from django.conf.urls import url

from django_event.publisher.views import event_list
from django_event.publisher.views import event_detail
from django_event.publisher.views import event_types
from django_event.publisher.views import cancel_event
from django_event.publisher.views import retry_event


urlpatterns = patterns(
    '',
    url(
        r'^$',
        event_list,
        name='event_list'
    ),
    url(
        r'^(?P<pk>[0-9]+)/$',
        event_detail,
        name='event_detail'
    ),
    url(
        r'^types/$',
        event_types,
        name='event_types'
    ),
    url(
        r'^(?P<pk>[0-9]+)/cancel/$',
        cancel_event,
        name='cancel_event'
    ),
    url(
        r'^(?P<pk>[0-9]+)/retry/$',
        retry_event,
        name='retry_event'
    ),
)