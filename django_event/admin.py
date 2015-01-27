# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Event


@admin.register(Event)
class SavedReportsAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'type',
        'status',
        'result',

        'created_at',
        'started',
        'started_at',
        'completed',
        'completed_at',

        'canceled',
        'retried',
        'viewed',
    )
    list_display_links = ('user', )