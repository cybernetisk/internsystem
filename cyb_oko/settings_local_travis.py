# this should be unique
SECRET_KEY = 'FCaHtnJn1mt4Ph5GY6ohQPz00mV96Ot1'

# see https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-DEBUG
DEBUG = True

# don't activate SAML on Travis (avoid the huge dependencies it has)
ENABLE_SAML = False
