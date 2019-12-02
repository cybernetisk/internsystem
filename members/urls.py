from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
from members.rest import MemberViewSet, MemberStatsViewSet

router = SharedAPIRootRouter()

router.register(r"member/members", MemberViewSet, basename="member-members")
router.register(r"member/stats", MemberStatsViewSet, basename="member-stats")
