"""
Django settings for cyb_oko project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import importlib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "oauth2_provider",
    "core",
    "varer",
    "cal",
    "voucher",
    "members",
    "intern",
    "django_filters",
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    # 'cyb_oko.querydebug.QueryCountDebugMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
)

AUTHENTICATION_BACKENDS = (
    "oauth2_provider.backends.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend",
    "samlauth.auth_backend.SAMLServiceProviderBackend",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
            # debug option is set later in this settings file
        },
    },
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ROOT_URLCONF = "cyb_oko.urls"

WSGI_APPLICATION = "cyb_oko.wsgi.application"

# custom User model
AUTH_USER_MODEL = "core.User"

CORS_ORIGIN_WHITELIST = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://internt.cyb.no",
    "https://cyb.no",
    "https://dev.internt.cyb.no",
    "https://test.in.cyb.no",
)
CORS_ALLOW_CREDENTIALS = True

# Disable SameSite for session and csrf cookie as we need this
# for auth to work when using local development server
# of frontend.
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SAMESITE = None

CSRF_TRUSTED_ORIGINS = [
    "https://dev.internt.cyb.no",
    "https://test.in.cyb.no",
    "http://localhost:3000",
]


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "cyb_oko", "db.sqlite3"),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = "nb"

TIME_ZONE = "Europe/Oslo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = "/static/"

# where settings.json is located for SAML-package
SAML_FOLDER = os.path.join(BASE_DIR, "samlauth", "dev")

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        # 'rest_framework.filters.DjangoFilterBackend',
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "cyb_oko.pagination.CybPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

CYB = {
    "CALENDAR": {
        "public": [
            "https://wiki.cyb.no/rest/calendar-services/1.0/calendar/export/subcalendar/private/ffb4f4ef5c35da9b4cfaa276a3a842051848632b.ics"
        ],
        "intern": [
            "https://wiki.cyb.no/rest/calendar-services/1.0/calendar/export/subcalendar/private/6e360b4215ee97862fecec0d4319d86a8feb364d.ics"
        ],
    }
}


# see https://docs.djangoproject.com/en/1.8/ref/settings/#secure-proxy-ssl-header
# if using nginx, make sure to have 'proxy_set_header X-Forwarded-Proto $scheme;' in config
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEBUG = False

# Use the SAML-module? Requires compiling of more requirements
# turn off in local settings if needed
ENABLE_SAML = True

OAUTH2_PROVIDER = {
    "SCOPES": {
        "none": "Read-only access to user details",
        "vouchers": "Access to modify vouchers",
        "members": "Access to modify the member register",
        "all": "Access to all resources the user have access to",
    },
}

# Local settings should be defined in the file `settings_local.py`
# It must at least contain `SECRET_KEY`
settings_local_name = os.getenv("LOCAL_SETTINGS", "settings_local")
if not os.path.isfile(os.path.dirname(__file__) + "/" + settings_local_name + ".py"):
    raise Exception("Missing local settingsfile. See settings.py")

locals().update(importlib.import_module("cyb_oko." + settings_local_name).__dict__)
if "SECRET_KEY" not in locals():
    raise Exception("Missing SECRET_KEY in local settings. See settings.py")

LOGIN_REDIRECT_URL = "/profile"
LOGIN_URL = "/saml/?sso" if ENABLE_SAML else "/api-auth/login/"
LOGOUT_URL = "/saml/sls/" if ENABLE_SAML else "/api-auth/logout/"

TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

if ENABLE_SAML:
    INSTALLED_APPS += ("samlauth",)
