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


class WorkLogCreateSerializer(serializers.Serializer):
    user = serializers.CharField()
    date_worked = serializers.DateField()
    work_group = serializers.CharField(max_length=20)
    hours = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)
    issuing_user = serializers.CharField()
    comment = serializers.CharField(max_length=100, required=False)


class WorkLogSerializer(serializers.ModelSerializer):
    wallet = VoucherWalletSerializer()

    class Meta:
        model = WorkLog
        fields = ('id', 'wallet', 'date_issued', 'date_worked', 'work_group',
                  'hours', 'vouchers', 'issuing_user', 'comment',)


class UseVouchersSerializer(serializers.Serializer):
    vouchers = serializers.IntegerField()
    comment = serializers.CharField()


class WalletStatsSerializer(serializers.Serializer):
    semester = SemesterSerializer()
    sum_balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_hours = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers_used = serializers.IntegerField()
    count_users = serializers.IntegerField()
