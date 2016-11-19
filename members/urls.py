from core.utils import SharedAPIRootRouter
from members.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()

router.register(r'member/members', MemberViewSet, base_name='member-members')
router.register(r'member/stats', MemberStatsViewSet, base_name='member-stats')
