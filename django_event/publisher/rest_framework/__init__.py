
"""
Django rest_framework required for this package.
"""

try:
    __import__('rest_framework')
except ImportError:
    raise ImportError(
        'Django rest_framework required for '
        'django_event.publisher.rest_framework package.'
    )