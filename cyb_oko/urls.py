from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from django.conf import settings

from varer.rest import *
from siteroot.views import angular_frontend

if settings.ENABLE_SAML:
    from samlauth import urls as samlauth_urls

from core.urls import urlpatterns as core_urlpatterns

router = routers.DefaultRouter()
router.register(r'kontoer', KontoViewSet)
router.register(r'råvarer', RåvareViewSet)
router.register(r'leverandører', LeverandørViewSet)
router.register(r'råvarepriser', RåvareprisViewSet)
router.register(r'salgsvarer', SalgsvareViewSet)
router.register(r'salgsvareråvarer', SalgsvareRåvareViewSet)
router.register(r'salgsvarepriser', SalgsvarePrisViewSet)
router.register(r'salgskalkyler', SalgskalkyleViewSet)
router.register(r'salgskalkylevarer', SalgskalkyleVareViewSet)
router.register(r'varetellinger', VaretellingViewSet)
router.register(r'varetellingvarer', VaretellingVareViewSet)

urlpatterns = []

if settings.ENABLE_SAML:
    urlpatterns += [url(r'^saml/', include(samlauth_urls.urlpatterns)),]

urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile$', angular_frontend, name='profile'),
]

urlpatterns += core_urlpatterns

urlpatterns += [
    url(r'^.*', angular_frontend),
]
