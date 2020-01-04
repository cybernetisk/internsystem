from cal.rest import UpcomingRemoteEventViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r"cal/upcoming", UpcomingRemoteEventViewSet, basename="cal_upcoming")
