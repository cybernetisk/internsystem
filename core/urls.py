from django.urls import re_path
from core.views import me

from core.rest import CardViewSet, UserViewSet, NfcCardViewSet, GroupViewSet
from core.utils import SharedAPIRootRouter

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r"core/users", UserViewSet, basename="users")
router.register(r"core/cards", CardViewSet, basename="voucher_cards")
router.register(r"core/nfc", NfcCardViewSet)
router.register(r"core/groups", GroupViewSet)

urlpatterns = [
    re_path(r"^api/me$", me, name="me"),
]
