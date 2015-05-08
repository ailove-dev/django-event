# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ...utils import try_import_or_runtime_error


try_import_or_runtime_error('pika',
    'Trying to use rabbitmq client without pika installed. Install pika to use '
    'this package.'
)