from core.utils import SharedAPIRootRouter
from voucher.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'voucher/cards', CardViewSet, base_name='voucher_cards')
router.register(r'voucher/wallets', VoucherWalletViewSet, base_name='voucher_wallets')
router.register(r'voucher/users', VoucherUserViewSet, base_name='voucher_users')
