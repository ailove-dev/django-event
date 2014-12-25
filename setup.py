from distutils.core import setup

import sys

from django_event import version, release_tag


requirments = [
    'django>=1.7',
    'celery>=3.1.16',
    'tornado>=4.0.2',
    'sockjs-tornado>=1.0.1',
    'pika>=0.9.14',
]

if sys.version < '3':
    requirments.extend([
        'futures>=2.2.0' # 2.7 backport of concurrent package
    ])


extras = {
    'rest_framework_api': ['djangorestframework>=2.3.14',]
}

setup_options = dict(
    name='django-event',
    version='%s-%s' % (version, release_tag) if release_tag else version,
    url='https://github.com/ailove-dev/django-event',
    license='MIT',
    author='Dmitry Panchenko',
    author_email='d.panchenko@ailove.com',
    description='Event notification system for django project',
    packages=['django_event'],
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
    extras_require=extras,
)

setup(**setup_options)
