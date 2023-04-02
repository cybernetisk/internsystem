from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from math import floor

from django.db.models import Sum, Count
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.models import Semester, NfcCard, User
from core.utils import get_semester_of_date
from voucher.filters import (
    WorkLogFilter,
    VoucherUseLogFilter,
    VoucherWalletFilter,
    CoffeeWalletFilter,
    CoffeeRegisterLogFilter,
    CoffeeUseLogFilter,
)
from voucher.models import (
    VoucherWallet,
    CoffeeWallet,
    WorkLog,
    VoucherUseLog,
    CoffeeRegisterLog,
    CoffeeUseLog,
)
from voucher.permissions import RegisterLogPermissions
from voucher.serializers import (
    WorkGroupsSerializer,
    CoffeeUseLogSerializer,
    VoucherUseLogSerializer,
    WorkLogSerializer,
    WorkLogCreateSerializer,
    RegisterLogSerializer,
    RegisterLogCreateSerializer,
    UseCoffeeVouchersSerializer,
    UseVouchersSerializer,
    WalletStatsSerializer,
    CoffeeWalletSerializer,
    VoucherWalletStatsSerializer,
    VoucherWalletSerializer,
)
from voucher.utils import get_valid_semesters


class VoucherWalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoucherWalletSerializer
    filter_class = VoucherWalletFilter

    def get_queryset(self):
        queryset = VoucherWallet.objects.all()
        if self.action == "stats":
            return queryset.order_by()
        return queryset.prefetch_related("user", "semester")

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # pull stuff from main table
        wallets1 = (
            self.get_queryset()
            .values("semester")
            .order_by("-semester__year", "-semester__semester")
            .annotate(
                sum_balance=Sum("cached_balance"),
                count_users=Count("user", distinct=True),
            )
        )

        # pull stuff from worklogs
        wallets2 = (
            self.get_queryset()
            .values("semester")
            .annotate(
                sum_hours=Sum("worklogs__hours"), sum_vouchers=Sum("worklogs__vouchers")
            )
        )

        # pull stuff from uselogs
        wallets3 = (
            self.get_queryset()
            .values("semester")
            .annotate(sum_vouchers_used=Sum("uselogs__vouchers"))
        )

        semesters = {}
        for semester in Semester.objects.all():
            semesters[semester.id] = semester

        data = OrderedDict()
        for row in wallets1:
            row["semester"] = semesters[row["semester"]]
            data[row["semester"].id] = row
        for row in wallets2:
            row["semester"] = semesters[row["semester"]]
            data[row["semester"].id].update(row)
        for row in wallets3:
            row["semester"] = semesters[row["semester"]]
            data[row["semester"].id].update(row)

        serializer = VoucherWalletStatsSerializer(data.values(), many=True)
        return Response(serializer.data)


class CoffeeWalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoffeeWalletSerializer
    filter_class = CoffeeWalletFilter

    def get_queryset(self):
        queryset = CoffeeWallet.objects.all()
        if self.action == "stats":
            return queryset
        return queryset.prefetch_related("card", "semester")

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # pull stuff from main table
        wallets1 = (
            self.get_queryset()
            .values("semester")
            .order_by("-semester__year", "-semester__semester")
            .annotate(
                sum_balance=Sum("cached_balance"),
                count_users=Count("user", distinct=True),
            )
        )

        # pull stuff from uselogs
        wallets2 = (
            self.get_queryset()
            .values("semester")
            .annotate(sum_vouchers_used=Sum("uselogs__vouchers"))
        )

        semesters = {}
        for semester in Semester.objects.all():
            semesters[semester.id] = semester

        data = OrderedDict()
        for row in wallets1:
            row["semester"] = semesters[row["semester"]]
            data[row["semester"].id] = row
        for row in wallets2:
            row["semester"] = semesters[row["semester"]]
            data[row["semester"].id].update(row)

        serializer = WalletStatsSerializer(data.values(), many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        return UseVouchersSerializer

    @action(detail=True, methods=["post"])
    def use_vouchers(self, request, username=None):
        user = self.get_object()
        # default ordering of semesters is descending in time, we need to be ascending
        # (see Meta-class of Semester)
        wallets = VoucherWallet.objects.filter(
            user=user, semester__in=get_valid_semesters()
        ).order_by("-semester")
        pending_transactions = []

        data = UseVouchersSerializer(data=request.data, context=self)
        data.is_valid(raise_exception=True)

        vouchers_to_spend = data.validated_data["vouchers"]

        # we are in a risk of a race condition if multiple requests occur at the same time
        # leaving a negative balance - but the risk is low and it is not critical, so we have
        # not tried to properly solve it
        available_vouchers = 0
        for wallet in wallets:
            if vouchers_to_spend == 0:
                break

            # balance is a decimal field, might be between 0 and 1
            if wallet.calculate_balance() < 1:
                continue

            available_vouchers += floor(wallet.cached_balance)
            new_log_entry = VoucherUseLog(
                issuing_user=request.user,
                wallet=wallet,
                comment=data.data["comment"],
                vouchers=min(vouchers_to_spend, floor(wallet.cached_balance)),
            )

            vouchers_to_spend -= new_log_entry.vouchers
            pending_transactions.append(new_log_entry)

        if vouchers_to_spend != 0:
            return Response(
                {
                    "error": _(
                        "User does not have enough vouchers. Currently having %d available."
                        % available_vouchers
                    )
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        for p in pending_transactions:
            p.save()

        return Response(
            [VoucherUseLogSerializer(p).data for p in pending_transactions],
            status=status.HTTP_201_CREATED,
        )


class CardViewSet(viewsets.GenericViewSet):
    queryset = NfcCard.objects.all()
    lookup_field = "card_uid"
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = UseVouchersSerializer

    @action(detail=True, methods=["post"])
    def use_vouchers(self, request, card_uid):
        card = self.get_object()
        wallets = CoffeeWallet.objects.filter(
            card=card, semester__in=get_valid_semesters()
        ).order_by("semester")
        pending_transactions = []

        data = UseCoffeeVouchersSerializer(data=request.data, context=self)
        data.is_valid(raise_exception=True)

        vouchers_to_spend = data.validated_data["vouchers"]

        # we are in a risk of a race condition if multiple requests occur at the same time
        # leaving a negative balance - but the risk is low and it is not critical, so we have
        # not tried to properly solve it
        available_vouchers = 0
        for wallet in wallets:
            if vouchers_to_spend == 0:
                break

            if wallet.calculate_balance() <= 0:
                continue

            available_vouchers += wallet.cached_balance
            new_log_entry = CoffeeUseLog(
                issuing_user=request.user,
                wallet=wallet,
                comment=data.data["comment"],
                vouchers=min(vouchers_to_spend, wallet.cached_balance),
            )

            vouchers_to_spend -= new_log_entry.vouchers
            pending_transactions.append(new_log_entry)

        if vouchers_to_spend != 0:
            return Response(
                {
                    "error": _(
                        "User does not have enough vouchers. Currently having %d available."
                        % available_vouchers
                    )
                },
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )

        for p in pending_transactions:
            p.save()

        return Response(
            [CoffeeUseLogSerializer(p).data for p in pending_transactions],
            status=status.HTTP_201_CREATED,
        )


class CoffeeRegisterLogViewSet(viewsets.ModelViewSet):
    queryset = CoffeeRegisterLog.objects.prefetch_related(
        "wallet__card", "wallet__semester", "issuing_user"
    ).all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        RegisterLogPermissions,
    )
    filter_class = CoffeeRegisterLogFilter
    ordering_fields = (
        "id",
        "wallet",
        "date_issued",
        "vouchers",
        "issuing_user",
        "can_edit",
        "can_delete",
    )

    def get_serializer_class(self):
        if self.action in ["create"]:
            return RegisterLogCreateSerializer
        else:
            return RegisterLogSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_uid = serializer.data["card"].strip().lower()
        card = NfcCard.objects.get_or_create(card_uid=card_uid)[0]
        if not card:
            raise ValidationError(
                detail=_("Card %(card)s not found")
                % {"card": serializer.data["card_uid"]}
            )

        wallet = CoffeeWallet.objects.get_or_create(
            card=card, semester=get_semester_of_date(datetime.now().date())
        )[0]

        registerlog = CoffeeRegisterLog(
            wallet=wallet,
            vouchers=Decimal(serializer.data["vouchers"]),
            issuing_user=request.user,
            comment=serializer.data["comment"],
        )

        registerlog.clean()
        registerlog.save()
        return Response(
            RegisterLogSerializer(registerlog, context={"request": self.request}).data,
            status=status.HTTP_201_CREATED,
        )


class WorkLogViewSet(viewsets.ModelViewSet):
    queryset = WorkLog.objects.prefetch_related(
        "wallet__user", "wallet__semester", "issuing_user"
    ).all()
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        RegisterLogPermissions,
    )
    filter_class = WorkLogFilter
    ordering_fields = ("date_issued", "date_worked", "work_group", "hours", "vouchers")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return WorkLogCreateSerializer
        else:
            return WorkLogSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data["user"].strip().lower()
        user = User.objects.get_or_create(username=username)[0]
        if not user:
            raise ValidationError(
                detail=_("User %(user)s not found") % {"user": serializer.data["user"]}
            )

        date = serializer.validated_data["date_worked"]
        wallet = VoucherWallet.objects.get_or_create(
            user=user, semester=get_semester_of_date(date)
        )[0]

        worklog = WorkLog(
            wallet=wallet,
            date_worked=serializer.data["date_worked"],
            work_group=serializer.data["work_group"],
            hours=Decimal(serializer.data["hours"]),
            issuing_user=request.user,
            comment=serializer.data["comment"],
        )

        worklog.clean()
        worklog.save()
        return Response(
            WorkLogSerializer(worklog, context={"request": self.request}).data,
            status=status.HTTP_201_CREATED,
        )


class VoucherUseLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoucherUseLogSerializer
    queryset = VoucherUseLog.objects.prefetch_related(
        "wallet__user", "wallet__semester"
    ).all()
    filter_class = VoucherUseLogFilter


class CoffeeUseLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CoffeeUseLogSerializer
    queryset = CoffeeUseLog.objects.prefetch_related(
        "wallet__card", "wallet__semester"
    ).all()
    filter_class = CoffeeUseLogFilter


class WorkGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkGroupsSerializer
    queryset = WorkLog.objects.order_by("work_group").distinct().values("work_group")
