from core.utils import SharedAPIRootRouter
from members.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()

router.register(r'member/semester', SemesterViewSet, base_name='semester')
router.register(r'member/member', MemberViewSet, base_name='member')
