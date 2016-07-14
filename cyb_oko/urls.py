from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from varer.rest import *



if settings.ENABLE_SAML:
    from samlauth import urls as samlauth_urls

from core.urls import urlpatterns as core_urlpatterns
import cal.urls  # do not remove, needed to load API-urls
import members.urls  # do not remove, needed to load API-urls
import varer.urls  # do not remove, needed to load API-urls
import voucher.urls  # do not remove, needed to load API-urls
import intern.urls  # do not remove, needed to load API-urls

from core.utils import SharedAPIRootRouter


router = SharedAPIRootRouter()

urlpatterns = []

if settings.ENABLE_SAML:
    urlpatterns += [url(r'^saml/', include(samlauth_urls.urlpatterns)),]
else:
    urlpatterns += [url(r'^saml/', RedirectView.as_view(url='/api-auth/login/', permanent=False, query_string=True)),]

urlpatterns += [
    url(r'^api/', include(router.shared_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^profile$', RedirectView.as_view(url='/api/me', permanent=False)),  # not used when having frontend
]

urlpatterns += core_urlpatterns
