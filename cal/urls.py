from django.conf.urls import patterns, url
from cal.rest import EventViewSet, SemesterViewSet, EscapeOccupiedViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'cal/events', EventViewSet, base_name='events')
router.register(r'cal/semesters', SemesterViewSet, base_name='semesters')
router.register(r'cal/escape_occupied', EscapeOccupiedViewSet, base_name='escape_occupied')

urlpatterns = patterns('',
    url(r'^cal/events\.ics$', 'cal.views.events_ics'),
    url(r'^cal/events/(\d+)\.ics$', 'cal.views.event_ics'),
)
