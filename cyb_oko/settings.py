"""
Django settings for cyb_oko project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, importlib
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
    'corsheaders',
    'rest_framework',
    'oauth2_provider',
    'core',
    'varer',
    'cal',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'cyb_oko.querydebug.QueryCountDebugMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    'samlauth.auth_backend.SAMLServiceProviderBackend',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'cyb_oko.urls'

WSGI_APPLICATION = 'cyb_oko.wsgi.application'

# custom User model
AUTH_USER_MODEL = 'core.User'

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000',
    'internt.cyb.no',
    'dev.internt.cyb.no',
)
CORS_ALLOW_CREDENTIALS = True

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

# where settings.json is located for SAML-package
SAML_FOLDER = os.path.join(BASE_DIR, 'samlauth')

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

# see https://docs.djangoproject.com/en/1.8/ref/settings/#secure-proxy-ssl-header
# if using nginx, make sure to have 'proxy_set_header X-Forwarded-Proto $scheme;' in config
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = False

# Use the SAML-module? Requires compiling of more requirements
# turn off in local settings if needed
ENABLE_SAML = True

# Local settings should be defined in the file `settings_local.py`
# It must at least contain `SECRET_KEY`
settings_local_name = os.getenv("LOCAL_SETTINGS", "settings_local")
if not os.path.isfile(os.path.dirname(__file__) + '/' + settings_local_name + '.py'):
    raise Exception("Missing local settingsfile. See settings.py")

locals().update(importlib.import_module('cyb_oko.' + settings_local_name).__dict__)
if not 'SECRET_KEY' in locals():
    raise Exception("Missing SECRET_KEY in local settings. See settings.py");

TEMPLATE_DEBUG = DEBUG

if ENABLE_SAML:
    INSTALLED_APPS += ('samlauth',)
