from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^events\.ics$', 'cal.views.events_ics'),
    url(r'^events/(\d+)\.ics$', 'cal.views.event_ics'),
)
