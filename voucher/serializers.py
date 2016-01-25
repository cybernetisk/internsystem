from rest_framework import serializers

from voucher.models import *
from core.serializers import UserSimpleSerializer, SemesterSerializer


class VoucherWalletSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    semester = SemesterSerializer()

    class Meta:
        model = VoucherWallet
        fields = ('id', 'user', 'semester', 'cached_balance',)


class VoucherUseLogSerializer(serializers.ModelSerializer):
    wallet = VoucherWalletSerializer()

    class Meta:
        model = VoucherUseLog
        fields = ('id', 'wallet', 'date_spent', 'comment', 'vouchers',)


class WorkLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLog
        fields = ('id', 'date_issued', 'date_worked', 'work_group', 'hours', 'vouchers', 'issuing_user', 'comment',)


class UseVouchersSerializer(serializers.Serializer):
    vouchers = serializers.IntegerField()
    comment = serializers.CharField()


class WalletStatsSerializer(serializers.Serializer):
    semester = SemesterSerializer()
    sum_balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    count_users = serializers.IntegerField()
