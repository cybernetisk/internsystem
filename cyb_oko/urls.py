from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView

from varer.rest import *

if settings.ENABLE_SAML:
    from samlauth import urls as samlauth_urls

from core.urls import urlpatterns as core_urlpatterns
import cal.urls  # do not remove, needed to load API-urls

from core.utils import SharedAPIRootRouter

router = SharedAPIRootRouter()

# TODO: namespace these API-endpoints and move it to the application urls-file
router.register(r'kontoer', KontoViewSet)
router.register(r'råvarer', RåvareViewSet)
router.register(r'leverandører', LeverandørViewSet)
router.register(r'råvarepriser', RåvareprisViewSet)
router.register(r'salgsvarer', SalgsvareViewSet)
router.register(r'salgsvareråvarer', SalgsvareRåvareViewSet)
router.register(r'salgsvarepriser', SalgsvarePrisViewSet)
router.register(r'salgskalkyler', SalgskalkyleViewSet, base_name='salgskalkyler')
router.register(r'salgskalkylevarer', SalgskalkyleVareViewSet)
router.register(r'varetellinger', VaretellingViewSet)
router.register(r'varetellingvarer', VaretellingVareViewSet)

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
