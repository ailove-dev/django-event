"""
Django settings for testproj project.

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
SECRET_KEY = 'yp0v^uq@nmrzwx&5dx)7#4n0b3aq5*jmhtd=0^_$yt_@$!v$54'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_event',
)

DJANGO_EVENT = {
    'BACKEND': 'rabbitmq',
    'BACKEND_OPTIONS': {
        'HOST': 'localhost',
        'PORT': 5672,
        'VIRTUAL_HOST': '',
        'USERNAME': '',
        'PASSWORD': '',
        'QUEUE_NAME': 'default',
    },

    # 'BACKEND': 'redis',
    # 'BACKEND_OPTIONS': {
    #     'HOST': 'localhost',
    #     'PORT': 6379,
    #     'PASSWORD': '',
    #     'DB': 0,
    #     'USE_REDIS_CACHE': False,
    #     'SOCKET_TIMEOUT': 5,
    #     'SOCKET_CONNECT_TIMEOUT': 5,
    #     'UNIX_SOCKET_PATH': None
    # },

    'TORNADO_OPTIONS': {
        'HOST': '/',
        'PORT': 8989
    },
    'LISTENERS': {
        'example_event_type':
        'django_event.subscriber.listeners.SendMessageListener',
    },
    'STORE_DAYS': 7,
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'testproj.urls'

WSGI_APPLICATION = 'testproj.wsgi.application'


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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
