from django.contrib import admin
from voucher.models import VoucherWallet, WorkLog, VoucherUseLog


class VoucherWalletAdmin(admin.ModelAdmin):
    model = VoucherWallet
    readonly_fields = ('cached_balance',)


admin.site.register(VoucherWallet, VoucherWalletAdmin)
admin.site.register(WorkLog)
admin.site.register(VoucherUseLog)
