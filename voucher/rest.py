from collections import OrderedDict
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Count
from decimal import Decimal

from voucher.serializers import *
from voucher.models import Wallet, WorkLog, UseLog
from voucher.filters import UseLogFilter, WalletFilter, WorkLogFilter
from voucher.permissions import WorkLogPermissions
from voucher.utils import get_valid_semesters
from core.utils import get_semester_of_date
from core.models import Semester


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletSerializer
    filter_class = WalletFilter
    queryset = Wallet.objects.prefetch_related('user', 'semester').all()

    @list_route(methods=['get'])
    def stats(self, request):
        # pull stuff from main table
        wallets1 = self.get_queryset() \
            .values('semester') \
            .order_by('-semester__year', '-semester__semester') \
            .annotate(sum_balance=Sum('cached_balance'),
                      count_users=Count('user', distinct=True))

        # pull stuff from worklogs
        wallets2 = self.get_queryset() \
            .values('semester') \
            .annotate(sum_hours=Sum('worklogs__hours'),
                      sum_vouchers=Sum('worklogs__vouchers'))

        # pull stuff from uselogs
        wallets3 = self.get_queryset() \
            .values('semester') \
            .annotate(sum_vouchers_used=Sum('uselogs__vouchers'))

        semesters = {}
        for semester in Semester.objects.all():
            semesters[semester.id] = semester

        data = OrderedDict()
        for row in wallets1:
            row['semester'] = semesters[row['semester']]
            data[row['semester'].id] = row
        for row in wallets2:
            row['semester'] = semesters[row['semester']]
            data[row['semester'].id].update(row)
        for row in wallets3:
            row['semester'] = semesters[row['semester']]
            data[row['semester'].id].update(row)

        serializer = WalletStatsSerializer(data.values(), many=True)
        return Response(serializer.data)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return UseVouchersSerializer

    @detail_route(methods=['post'])
    def use_vouchers(self, request, username=None):
        user = self.get_object()
        wallets = Wallet.objects.filter(user=user, semester__in=get_valid_semesters()).order_by('semester')
        pending_transactions = []

        data = UseVouchersSerializer(data=request.data, context=self)
        data.is_valid(raise_exception=True)

        vouchers_to_spend = data.validated_data['vouchers']

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
            new_log_entry = UseLog(issuing_user=request.user,
                                   wallet=wallet,
                                   comment=data.data['comment'],
                                   vouchers=min(vouchers_to_spend, wallet.cached_balance))

            vouchers_to_spend -= new_log_entry.vouchers
            pending_transactions.append(new_log_entry)

        if vouchers_to_spend != 0:
            return Response(
                {'error': _('User does not have enough vouchers. Currently having %d available.' % available_vouchers)},
                status=status.HTTP_402_PAYMENT_REQUIRED
            )

        for p in pending_transactions:
            p.save()

        return Response([UseLogSerializer(p).data for p in pending_transactions], status=status.HTTP_201_CREATED)


class WorkLogViewSet(viewsets.ModelViewSet):
    queryset = WorkLog.objects.prefetch_related('wallet__user', 'wallet__semester', 'issuing_user').all()
    permission_classes = (IsAuthenticatedOrReadOnly, WorkLogPermissions,)
    filter_class = WorkLogFilter

    def get_serializer_class(self):
        if self.action in ['create']:
            return WorkLogCreateSerializer
        else:
            return WorkLogSerializer

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.data['user'].strip()
        user = User.objects.get_or_create(username=username)[0]
        if not user:
            raise ValidationError(detail=_('User %(user)s not found') % {'user': serializer.data['user']})

        date = serializer.validated_data['date_worked']
        wallet = Wallet.objects.get_or_create(user=user, semester=get_semester_of_date(date))[0]

        worklog = WorkLog(
            wallet=wallet,
            date_worked=serializer.data['date_worked'],
            work_group=serializer.data['work_group'],
            hours=Decimal(serializer.data['hours']),
            issuing_user=request.user,
            comment=serializer.data['comment']
        )

        worklog.clean()
        worklog.save()
        return Response(WorkLogSerializer(worklog).data, status=status.HTTP_201_CREATED)


class UseLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UseLogSerializer
    queryset = UseLog.objects.prefetch_related('wallet__user', 'wallet__semester').all()
    filter_class = UseLogFilter


class WorkGroupsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkGroupsSerializer
    queryset = WorkLog.objects.order_by('work_group').distinct().values('work_group')
