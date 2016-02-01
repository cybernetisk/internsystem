from core.utils import SharedAPIRootRouter
from varer.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'varer/kontoer', KontoViewSet)
router.register(r'varer/råvarer', RåvareViewSet)
router.register(r'varer/leverandører', LeverandørViewSet)
router.register(r'varer/inprices', RåvareprisViewSet)
router.register(r'varer/salgsvarer', SalgsvareViewSet)
router.register(r'varer/salgsvareråvarer', SalgsvareRåvareViewSet)
router.register(r'varer/salgsvarepriser', SalgsvarePrisViewSet)
router.register(r'varer/salgskalkyler', SalgskalkyleViewSet, base_name='salgskalkyler')
router.register(r'varer/salgskalkylevarer', SalgskalkyleVareViewSet)
router.register(r'varer/varetellinger', VaretellingViewSet)
router.register(r'varer/varetellingvarer', VaretellingVareViewSet)
