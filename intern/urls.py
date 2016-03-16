from core.utils import SharedAPIRootRouter

from intern.rest import InternViewSet

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'intern/interns', InternViewSet, base_name='interns')
