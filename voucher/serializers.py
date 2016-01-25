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
        fields = ('wallet', 'date_spent', 'comment', 'vouchers',)


class VoucherSerializer(serializers.Serializer):
    vouchers = serializers.IntegerField()
    comment = serializers.CharField()


class WalletStatsSerializer(serializers.Serializer):
    semester = SemesterSerializer()
    sum_balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    count_users = serializers.IntegerField()
