from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from cyb_varer.varer.rest import *

router = routers.DefaultRouter()
router.register(r'api/kontoer', KontoViewSet)
router.register(r'api/råvarer', RåvareViewSet)
router.register(r'api/leverandører', LeverandørViewSet)
router.register(r'api/råvarepriser', RåvareprisViewSet)
router.register(r'api/salgsvarer', SalgsvareViewSet)
router.register(r'api/salgsvareråvarer', SalgsvareRåvareViewSet)
router.register(r'api/salgsvarepriser', SalgsvarePrisViewSet)
router.register(r'api/salgskalkyler', SalgskalkyleViewSet)
router.register(r'api/salgskalkylevarer', SalgskalkyleVareViewSet)
router.register(r'api/varetellinger', VaretellingViewSet)
router.register(r'api/varetellingvarer', VaretellingVareViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls))
]

