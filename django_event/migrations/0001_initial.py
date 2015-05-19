# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=30)),
                ('send_mail', models.BooleanField(default=False)),
                ('task_id', models.CharField(max_length=256, null=True)),
                ('task_name', models.CharField(max_length=256, editable=False)),
                ('event_request', models.TextField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(null=True)),
                ('completed_at', models.DateTimeField(null=True)),
                ('started', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
                ('retried', models.BooleanField(default=False)),
                ('viewed', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('result', models.TextField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
    ]
