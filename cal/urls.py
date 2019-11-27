from cal.rest import (
    EscapeOccupiedViewSet,
    EventViewSet,
    SemesterViewSet,
    UpcomingRemoteEventViewSet,
)
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'cal/events', EventViewSet, basename='events')
router.register(r'cal/semesters', SemesterViewSet, basename='semesters')
router.register(r'cal/escape_occupied', EscapeOccupiedViewSet, basename='escape_occupied')
router.register(r'cal/upcoming', UpcomingRemoteEventViewSet, basename='cal_upcoming')
