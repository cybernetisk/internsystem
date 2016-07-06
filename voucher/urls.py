from core.utils import SharedAPIRootRouter
from voucher.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'voucher/voucher/wallets', VoucherWalletViewSet, base_name='voucher_wallets')
router.register(r'voucher/coffee/wallets', CoffeeWalletViewSet, base_name='coffee_wallets')
router.register(r'voucher/voucher/registerlogs', VoucherRegisterLogViewSet)
router.register(r'voucher/coffee/registerlogs', CoffeeRegisterLogViewSet)
router.register(r'voucher/voucher/uselogs', VoucherUseLogViewSet)
router.register(r'voucher/coffee/uselogs', CoffeeUseLogViewSet)
router.register(r'voucher/users', UserViewSet, base_name='voucher_users')
router.register(r'voucher/workgroups', WorkGroupsViewSet, base_name='voucher_workgroups')
