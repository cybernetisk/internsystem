from core.utils import SharedAPIRootRouter
from voucher.rest import *

# SharedAPIRootRouter is automatically imported in global urls config
router = SharedAPIRootRouter()
router.register(r'voucher/wallets', VoucherWalletViewSet, basename='voucher_wallets')
router.register(r'coffee/wallets', CoffeeWalletViewSet, basename='coffee_wallets')
router.register(r'voucher/worklogs', WorkLogViewSet)
router.register(r'coffee/registerlogs', CoffeeRegisterLogViewSet)
router.register(r'voucher/uselogs', VoucherUseLogViewSet)
router.register(r'coffee/uselogs', CoffeeUseLogViewSet)
router.register(r'voucher/users', UserViewSet, basename='voucher_users')
router.register(r'coffee/cards', CardViewSet, basename='coffee_cards')
router.register(r'voucher/workgroups', WorkGroupsViewSet, basename='voucher_workgroups')
