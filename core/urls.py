from django.conf.urls import url
from core.views import me

from core.rest import CardViewSet, UserViewSet, NfcCardViewSet, GroupViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'core/users', UserViewSet, base_name='users')
router.register(r'core/cards', CardViewSet, base_name='voucher_cards')
router.register(r'core/nfc', NfcCardViewSet)
router.register(r'core/groups', GroupViewSet)

urlpatterns = [
    url(r'^api/me$', me, name='me'),
]
