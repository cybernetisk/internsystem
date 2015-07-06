# this should be unique
SECRET_KEY = 'edit-me'

# see https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-DEBUG
DEBUG = True

# enable SAML if wanted
# see setup_saml.sh
ENABLE_SAML = False

# see https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-ALLOWED_HOSTS
#ALLOWED_HOSTS = [
#    'something',
#]

# if collectstatic is used, set up this
#STATIC_ROOT = "/home/django/django_project/env/static/"

# example for postgres configuration
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'django',
#        'USER': 'django',
#        'PASSWORD': 'edit-me',
#        'HOST': '127.0.0.1',
#        'PORT': '5432',
#    }
#}

# to log the queries in console, uncomment this
#LOGGING = {
#    'version': 1,
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'class': 'logging.StreamHandler'
#        }
#    },
#    'loggers': {
#        'cyb_oko.querydebug': {
#            'handlers': ['console'],
#            'level': 'DEBUG'
#        },
#        'django.db.backends': {
#            'level': 'DEBUG',
#            'handlers': ['console']
#        }
#    }
#}
