from django.core import validators
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.serializers import NfcCardSerializer, SemesterSerializer, UserSimpleSerializer
from core.utils import get_semester_of_date
from voucher.models import (
    CoffeeRegisterLog,
    CoffeeUseLog,
    CoffeeWallet,
    VoucherUseLog,
    VoucherWallet,
    WorkLog,
)
from voucher.permissions import register_log_has_perm
from voucher.validators import ValidVouchers, valid_date_worked


class WalletSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()


class VoucherWalletSerializer(WalletSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = VoucherWallet
        fields = (
            "id",
            "user",
            "semester",
            "cached_balance",
            "cached_hours",
            "cached_vouchers",
            "cached_vouchers_used",
            "is_valid",
        )


class CoffeeWalletSerializer(WalletSerializer):
    card = NfcCardSerializer()

    class Meta:
        model = CoffeeWallet
        fields = (
            "id",
            "card",
            "semester",
            "cached_balance",
            "cached_vouchers",
            "cached_vouchers_used",
            "is_valid",
        )


class UseLogSerializer(serializers.ModelSerializer):
    issuing_user = UserSimpleSerializer(read_only=True)


class VoucherUseLogSerializer(UseLogSerializer):
    wallet = VoucherWalletSerializer()

    class Meta:
        model = VoucherUseLog
        fields = (
            "id",
            "wallet",
            "date_spent",
            "issuing_user",
            "comment",
            "vouchers",
        )


class CoffeeUseLogSerializer(UseLogSerializer):
    wallet = CoffeeWalletSerializer()

    class Meta:
        model = CoffeeUseLog
        fields = (
            "id",
            "wallet",
            "date_spent",
            "issuing_user",
            "comment",
            "vouchers",
        )


class RegisterLogCreateSerializer(serializers.Serializer):
    card = serializers.CharField(
        max_length=8,
        help_text=_("Required. 8 characters. Letters and digits only):"),
        validators=[
            validators.RegexValidator(
                r"^[\w]+$", _("Enter a valid username."), "invalid"
            )
        ],
    )
    vouchers = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)
    comment = serializers.CharField(max_length=100, allow_blank=True, default=None)


class WorkLogCreateSerializer(serializers.Serializer):
    user = serializers.CharField(
        max_length=30,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+-]+$", _("Enter a valid username."), "invalid"
            )
        ],
    )
    date_worked = serializers.DateField(validators=[valid_date_worked])
    work_group = serializers.CharField(max_length=20)
    hours = serializers.DecimalField(max_digits=8, decimal_places=2, min_value=0.01)
    comment = serializers.CharField(max_length=100, allow_blank=True, default=None)


class RegisterLogSerializer(serializers.ModelSerializer):
    wallet = CoffeeWalletSerializer(read_only=True)
    issuing_user = UserSimpleSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField("_can_edit")
    can_delete = serializers.SerializerMethodField("_can_delete")

    def _can_edit(self, instance):
        return register_log_has_perm(self.context["request"], instance, "change")

    def _can_delete(self, instance):
        return register_log_has_perm(self.context["request"], instance, "delete")

    class Meta:
        model = CoffeeRegisterLog
        fields = (
            "id",
            "wallet",
            "date_issued",
            "vouchers",
            "issuing_user",
            "comment",
            "can_edit",
            "can_delete",
        )
        read_only_fields = (
            "id",
            "wallet",
            "date_issued",
            "issuing_user",
        )

    def update(self, instance, validated_data):
        if (
            "vouchers" in validated_data
            or validated_data["vouchers"] != instance.vouchers
        ):
            instance.vouchers = int(validated_data["vouchers"])
            validated_data.pop("vouchers", None)

        return super().update(instance, validated_data)


class WorkLogSerializer(serializers.ModelSerializer):
    wallet = VoucherWalletSerializer(read_only=True)
    date_worked = serializers.DateField(validators=[valid_date_worked])
    issuing_user = UserSimpleSerializer(read_only=True)
    can_edit = serializers.SerializerMethodField("_can_edit")
    can_delete = serializers.SerializerMethodField("_can_delete")

    def _can_edit(self, instance):
        return register_log_has_perm(self.context["request"], instance, "change")

    def _can_delete(self, instance):
        return register_log_has_perm(self.context["request"], instance, "delete")

    class Meta:
        model = WorkLog
        fields = (
            "id",
            "wallet",
            "date_issued",
            "date_worked",
            "work_group",
            "hours",
            "vouchers",
            "issuing_user",
            "comment",
            "can_edit",
            "can_delete",
        )
        read_only_fields = (
            "id",
            "wallet",
            "date_issued",
            "issuing_user",
        )

    def update(self, instance, validated_data):
        if (
            "hours" in validated_data
            and validated_data["hours"] != instance.hours
            and (
                "vouchers" not in validated_data
                or validated_data["vouchers"] == instance.vouchers
            )
        ):
            instance.vouchers = instance.calculate_vouchers(validated_data["hours"])
            validated_data.pop("vouchers", None)

        if "date_worked" in validated_data:
            date = validated_data["date_worked"]
            wallet = VoucherWallet.objects.get_or_create(
                user=instance.wallet.user, semester=get_semester_of_date(date)
            )[0]
            instance.wallet = wallet

        return super().update(instance, validated_data)


class UseVouchersSerializer(serializers.ModelSerializer):
    vouchers = serializers.IntegerField(validators=[ValidVouchers()])

    class Meta:
        model = VoucherUseLog
        fields = (
            "vouchers",
            "comment",
        )
        extra_kwargs = {"comment": {"default": None}}


class UseCoffeeVouchersSerializer(serializers.ModelSerializer):
    vouchers = serializers.IntegerField(validators=[ValidVouchers()])

    class Meta:
        model = CoffeeUseLog
        fields = (
            "vouchers",
            "comment",
        )
        extra_kwargs = {"comment": {"default": None}}


class WalletStatsSerializer(serializers.Serializer):
    semester = SemesterSerializer()
    sum_balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers = serializers.DecimalField(max_digits=8, decimal_places=2)
    sum_vouchers_used = serializers.IntegerField()


class VoucherWalletStatsSerializer(WalletStatsSerializer):
    sum_hours = serializers.DecimalField(max_digits=8, decimal_places=2)
    count_users = serializers.IntegerField()


class WorkGroupsSerializer(serializers.Serializer):
    work_group = serializers.CharField()
