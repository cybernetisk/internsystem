from django.contrib import admin
from voucher.models import Wallet, VoucherRegisterLog, UseLog, VoucherWallet, CoffeeWallet, VoucherUseLog, CoffeeUseLog, \
    CoffeeRegisterLog


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    readonly_fields = ('cached_balance',)


admin.site.register(VoucherWallet, WalletAdmin)
admin.site.register(CoffeeWallet, WalletAdmin)
admin.site.register(CoffeeRegisterLog)
admin.site.register(VoucherRegisterLog)
admin.site.register(VoucherUseLog)
admin.site.register(CoffeeUseLog)
