from django.contrib import admin
from voucher.models import Wallet, WorkLog, UseLog, VoucherWallet, CoffeeWallet, VoucherUseLog, CoffeeUseLog, \
    RegisterLog


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    readonly_fields = ('cached_balance',)


admin.site.register(VoucherWallet, WalletAdmin)
admin.site.register(CoffeeWallet, WalletAdmin)
admin.site.register(RegisterLog)
admin.site.register(WorkLog)
admin.site.register(VoucherUseLog)
admin.site.register(CoffeeUseLog)
