from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Count

from voucher.serializers import *
from voucher.models import *
from voucher.filters import UseLogFilter, WorkLogFilter
from core.models import Card
from core.serializers import CardSerializer
from core.utils import get_semester


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Card.objects.all()
        cardnum = self.request.query_params.get('cardnum', None)

        if cardnum is not None:
            queryset = queryset.filter(card_number=cardnum)

        return queryset


class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletSerializer
    filter_fields = ('semester',)

    def get_queryset(self):
        cardnum = self.request.query_params.get('cardnum', None)
        username = self.request.query_params.get('username', None)

        queryset = Wallet.objects.prefetch_related('user', 'semester').all()

        if cardnum is not None:
            cards = Card.objects.filter(card_number=cardnum)
            if cards.exists():
                queryset = queryset.filter(user=cards.first().user)
            else:
                queryset = queryset.none()

        if username is not None:
            queryset = queryset.filter(user__username=username)

        return queryset

    @list_route(methods=['get'])
    def stats(self, request):
        # pull stuff from main table
        wallets1 = self.get_queryset() \
            .values('semester') \
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

        data = {}
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
        return None

    def get_valid_semesters(self):
        semesters = []
        now = datetime.now()
        if now.month == 8 or now.month == 1:
            semesters.append(get_semester(-1))
        semesters.append(get_semester())
        return semesters

    @detail_route(methods=['post'])
    def use_vouchers(self, request, username=None):
        user = self.get_object()
        wallets = Wallet.objects.filter(user=user, semester__in=self.get_valid_semesters()).order_by('semester')
        pending_transactions = []

        data = UseVouchersSerializer(data=request.data)

        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        vouchers_to_spend = data.data['vouchers']

        if vouchers_to_spend <= 0:
            return Response({'error': _('Vouchers must be positive')}, status=status.HTTP_400_BAD_REQUEST)

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
            new_log_entry = UseLog(wallet=wallet,
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

        return Response(
            {
                'status': 'ok',
                'transactions': [UseLogSerializer(p).data for p in pending_transactions]
            }
        )


class WorkLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkLog.objects.prefetch_related('wallet__user', 'wallet__semester', 'issuing_user').all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = WorkLogFilter

    def get_first_valid_date(self):
        valid = date.today().replace(day=1)

        if valid.month <= 1:
            valid = valid.replace(year=valid.year - 1)
            valid = valid.replace(month=7)
        elif valid.month <= 8:
            valid = valid.replace(month=1)
        else:
            valid = valid.replace(month=7)

        return valid

    def get_serializer_class(self):
        if self.action in ['create']:
            return WorkLogCreateSerializer
        else:
            return WorkLogSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        date = datetime.strptime(serializer.data['date_worked'], '%Y-%m-%d').date()
        if date < self.get_first_valid_date():
            return Response(
                {'error': _('Date %(date)s is too old') % {'date': serializer.data['date_worked']}},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        if date > date.today():
            return Response(
                {'error': _('Date %(date)s is in the future') % {'date': serializer.data['date_worked']}},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        username = serializer.data['user'].strip()
        user = User.objects.get_or_create(username=username)[0]
        if not user:
            return Response(
                {'error': _('User %(user)s not found') % {'user': serializer.data['user']}},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        wallet = Wallet.objects.get_or_create(user=user, semester=get_semester())[0]

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
