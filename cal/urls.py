from django.conf.urls import patterns, url
from cal.rest import EventViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'cal/events', EventViewSet)

urlpatterns = patterns('',
    url(r'^events\.ics$', 'cal.views.events_ics'),
    url(r'^events/(\d+)\.ics$', 'cal.views.event_ics'),
)
