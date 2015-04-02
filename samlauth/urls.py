from django.conf.urls import url, patterns
from django.views.decorators.csrf import csrf_exempt
from samlauth.views import sls, acs, index, metadata

urlpatterns = patterns('',
    # SingleLogoutService
    url(r'sls/$', csrf_exempt(sls), name='saml_sls'),

    # AssertionConsumerService
    url(r'acs/$', csrf_exempt(acs), name='saml_acs'),

    # Metadata
    url(r'^metadata/$', metadata, name='saml_metadata'),

    url(r'^$', index, name='saml_index'),
)
