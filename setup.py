# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
from setuptools import setup
from setuptools import find_packages

from django_event import __version__
from django_event import __release_tag__


requirments = [
    'django>=1.7',
    'celery>=3.1.16',
    'tornado>=4.0.2',
    'sockjs-tornado>=1.0.1',
]

if sys.version < '3':
    requirments.extend([
        'futures>=2.2.0'  # 2.7 backport of concurrent package
    ])


extras = {
    'rest_framework': ['djangorestframework>=3.1.1', ],
    'rabbit_mq': ['pika>=0.9.14', ],
    'redis': ['django-redis==3.8.3', ],
}

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    for extra_requirements in extras.itervalues():
        requirments.extend(extra_requirements)


setup_options = dict(
    name='django-event',
    version='%s-%s' % (
        __version__, __release_tag__
    ) if __release_tag__ else __version__,
    url='https://github.com/ailove-dev/django-event',
    license='MIT',
    author='Dmitry Panchenko',
    author_email='d.panchenko@ailove.com',
    description='Event notification system for django project',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirments,
    tests_require=['Django'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)

setup(**setup_options)
