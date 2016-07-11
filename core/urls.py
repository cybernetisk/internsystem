from django.conf.urls import url, patterns
from core.views import me

from core.rest import CardViewSet, UserViewSet, NfcCardViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'core/users', UserViewSet, base_name='users')
router.register(r'core/cards', CardViewSet, base_name='voucher_cards')
router.register(r'core/nfc', NfcCardViewSet)

urlpatterns = patterns('',
    url(r'^api/me$', me, name='me'),
)
