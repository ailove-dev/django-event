from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import *

urlpatterns = patterns(
    '',

    url(r'^example/', example),
    url(r'^example_start/', example_start),
)
