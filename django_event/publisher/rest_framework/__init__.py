# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ...utils import try_import_or_runtime_error


try_import_or_runtime_error('rest_framework',
    'Trying to use rest_framework depend package without rest_framework'
    'installed. Install djangorestframework to use this package.'
)