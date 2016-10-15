from django.contrib import admin
from voucher.models import Wallet, WorkLog, UseLog, VoucherWallet, CoffeeWallet, VoucherUseLog, CoffeeUseLog, \
    CoffeeRegisterLog


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    readonly_fields = ('cached_balance',)

class WorkLogAdmin(admin.ModelAdmin):
    model = WorkLog
    list_filter = ('wallet__user', 'work_group')
    list_display = ('wallet', 'hours', 'work_group')
    search_fields = ('wallet__user__username',)


admin.site.register(VoucherWallet, WalletAdmin)
admin.site.register(CoffeeWallet, WalletAdmin)
admin.site.register(CoffeeRegisterLog)
admin.site.register(WorkLog, WorkLogAdmin)
admin.site.register(VoucherUseLog)
admin.site.register(CoffeeUseLog)
