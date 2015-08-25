from django.conf.urls import url, patterns
from core.views import me

from core.rest import UserViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'core/users', UserViewSet, base_name='users')

urlpatterns = patterns('',
    url(r'^api/me$', me, name='me'),
)
