"""
Django settings for cyb_oko project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = [
    '*'
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'siteroot',
    'varer'
)

MIDDLEWARE_CLASSES = (
    'cyb_oko.querydebug.QueryCountDebugMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'cyb_oko.urls'

WSGI_APPLICATION = 'cyb_oko.wsgi.application'


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

LANGUAGE_CODE = 'nb'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "siteroot/static_build"),
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    #'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'limit',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_SERIALIZER_CLASS': 'cyb_oko.pagination.CybPaginationSerializer'
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'cyb_oko.querydebug': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}

DEBUG = False

# Local settings should be defined in the file `settings_local.py`
# It must at least contain `SECRET_KEY`
if not os.path.isfile(os.path.dirname(__file__) + '/settings_local.py'):
    raise Exception("Missing local settingsfile. See settings.py")

from cyb_oko.settings_local import *
if not 'SECRET_KEY' in locals():
    raise Exception("Missing SECRET_KEY in local settings. See settings.py");

TEMPLATE_DEBUG = DEBUG
