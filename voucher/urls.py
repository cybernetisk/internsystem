from core.utils import SharedAPIRootRouter
from voucher.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'nfc', CardViewSet, base_name='nfc')
router.register(r'voucher', VoucherWalletViewSet, base_name='nfc')
router.register(r'voucher', VoucherViewSet, base_name='nfc')