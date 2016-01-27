from django.contrib import admin
from voucher.models import Wallet, WorkLog, UseLog


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    readonly_fields = ('cached_balance',)


admin.site.register(Wallet, WalletAdmin)
admin.site.register(WorkLog)
admin.site.register(UseLog)
