"""
Django settings for django_event_example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's5yqa0o(=dvl36fi*pp%r!6=!2(m^51r)i%gu1o#w9^tb=nbf3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_event',
    'example',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_event_example.urls'

WSGI_APPLICATION = 'django_event_example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CACHES = {
    'default': '',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

CELERY_TIMEZONE = 'Europe/Moscow'

BROKER_URL = (
    'redis://localhost:6379/0'
)
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_DEFAULT_QUEUE = 'default'

# BROKER_URL = (
#     'amqp://purinaproplan:purinaproplan@localhost:5672/purinaproplan-dev'
# )
# CELERY_RESULT_BACKEND = 'amqp'
# CELERY_DEFAULT_QUEUE = 'default'


from .celery import *

DJANGO_EVENT = {
    # 'BACKEND': 'rabbitmq',
    # 'BACKEND_OPTIONS': {
    #     'HOST': 'localhost',
    #     'PORT': 5672,
    #     'VIRTUAL_HOST': 'default',
    #     'USERNAME': 'admin',
    #     'PASSWORD': 'admin',
    #     'QUEUE_NAME': 'default',
    # },

    'BACKEND': 'redis',
    'BACKEND_OPTIONS': {
        'HOST': 'localhost',
        'PORT': 6379,
        'PASSWORD': '',
        'DB': 0,
    },

    'TORNADO_OPTIONS': {
        'HOST': '',
        'PORT': 8989
    },
    'LISTENERS': {
        'example_event_type':
        'django_event.subscriber.listeners.SendMessageListener',
    },
    'STORE_DAYS': 7,
}
