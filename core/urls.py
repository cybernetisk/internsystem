from django.conf.urls import url, patterns
from core.views import me

urlpatterns = patterns('',
    url(r'^api/me$', me, name='me'),
)
