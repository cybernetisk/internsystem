from core.utils import SharedAPIRootRouter
from members.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
# TODO: Add endpoints under here.
router.register(r'member/members', MemberViewSet)
