from rest_framework import serializers
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from voucher.models import UseLog, Wallet, WorkLog
from voucher.utils import valid_date_worked
from core.models import User
from core.serializers import UserSimpleSerializer, SemesterSerializer
from core.utils import get_semester_of_date


class WalletSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    semester = SemesterSerializer()

    class Meta:
        model = Wallet
        fields = ('id', 'user', 'semester', 'cached_balance', 'is_valid',)


class UseLogSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = UseLog
        fields = ('id', 'wallet', 'date_spent', 'comment', 'vouchers',)


class WorkLogCreateSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=30,
                                 help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                             '@/./+/-/_ only.'),
                                 validators=[
                                     validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
                                 ])
    date_worked = serializers.DateField(validators=[valid_date_worked])
    work_group = serializers.CharField(max_length=20)
    hours = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)
    comment = serializers.CharField(max_length=100, allow_blank=True, default=None)


class WorkLogSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)
    issuing_user = UserSimpleSerializer(read_only=True)
    date_worked = serializers.DateField(validators=[valid_date_worked])

    class Meta:
        model = WorkLog
        fields = ('id', 'wallet', 'date_issued', 'date_worked', 'work_group',
                  'hours', 'vouchers', 'issuing_user', 'comment',)
        read_only_fields = ('id', 'wallet', 'date_issued', 'issuing_user',)

    def update(self, instance, validated_data):
        if 'hours' in validated_data and validated_data['hours'] != instance.hours and \
                ('vouchers' not in validated_data or validated_data['vouchers'] == instance.vouchers):
            instance.vouchers = instance.calculate_vouchers(validated_data['hours'])
            validated_data.pop('vouchers')

        if 'date_worked' in validated_data:
            date = validated_data['date_worked']
            wallet = Wallet.objects.get_or_create(user=instance.wallet.user, semester=get_semester_of_date(date))[0]
            instance.wallet = wallet

        return super().update(instance, validated_data)


class UseVouchersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseLog
        fields = ('vouchers', 'comment',)
        extra_kwargs = {'comment': {'default': None}}


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'realname',)


class WalletStatsSerializer(serializers.Serializer):
    semester = SemesterSerializer()
    sum_balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_hours = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers_used = serializers.IntegerField()
    count_users = serializers.IntegerField()
