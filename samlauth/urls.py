from django.views.decorators.csrf import csrf_exempt
from django.urls import re_path
from samlauth.views import sls, acs, index, metadata, sso

urlpatterns = [
    # SingleLogoutService
    re_path(r"sls/$", csrf_exempt(sls), name="saml_sls"),
    # AssertionConsumerService
    re_path(r"acs/$", csrf_exempt(acs), name="saml_acs"),
    # Metadata
    re_path(r"^metadata/$", metadata, name="saml_metadata"),
    re_path(r"^$", index, name="saml_index"),
    re_path(r"sso", sso, name="saml_sso"),
]
