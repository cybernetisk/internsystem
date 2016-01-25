from rest_framework import viewsets
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum, Count

from voucher.serializers import *
from voucher.models import *
from core.models import Card
from core.serializers import CardSerializer
from core.utils import get_semester


class UserFromCard(generics.RetrieveAPIView):
    def retrieve(request, *args, **kwargs):
        raise exceptions.NotAuthenticated()


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = Card.objects.all()
        cardnum = self.request.query_params.get('cardnum', None)

        if cardnum is not None:
            queryset = queryset.filter(card_number=cardnum)

        return queryset


class VoucherWalletViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoucherWalletSerializer

    filter_fields = ('semester',)

    def get_queryset(self):
        cardnum = self.request.query_params.get('cardnum', None)
        username = self.request.query_params.get('username', None)

        queryset = VoucherWallet.objects.all()

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
        queryset = self.get_queryset() \
            .values('semester') \
            .annotate(sum_balance=Sum('cached_balance'), count_users=Count('user'))

        semesters = {}
        for semester in Semester.objects.all():
            semesters[semester.id] = semester

        data = []
        for sem in queryset:
            sem['semester'] = semesters[sem['semester']]
            data.append(sem)

        serializer = WalletStatsSerializer(data, many=True)
        return Response(serializer.data)


class VoucherUserViewSet(viewsets.GenericViewSet):
    serializer_class = UseVouchersSerializer
    queryset = User.objects.all()

    def get_valid_semesters(self):
        semesters = []
        now = datetime.now()
        if now.month == 8 or now.month == 1:
            semesters.append(get_semester(-1))
        semesters.append(get_semester())
        return semesters

    @detail_route(methods=['post'])
    def use_vouchers(self, request):
        user = self.get_object()
        wallets = VoucherWallet.objects.filter(user=user, semester__in=self.get_valid_semesters()).order_by('semester')
        pending_transactions = []

        data = UseVouchersSerializer(data=request.data)

        if not data.is_valid():
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

        vouchers_used = 0
        vouchers_to_spend = data.data['vouchers']

        if vouchers_to_spend <= 0:
            return Response({'error': _('Vouchers must be positive')}, status=status.HTTP_400_BAD_REQUEST)

        for w in wallets:
            if vouchers_to_spend == 0:
                break

            w.calculate_balance()

            new_log_entry = VoucherUseLog(wallet=w,
                                          comment=data.data['comment'],
                                          vouchers=min(vouchers_to_spend, w.cached_balance))

            vouchers_to_spend -= new_log_entry.vouchers
            pending_transactions.append(new_log_entry)

        if vouchers_to_spend != 0:
            return Response({'error': _('User does not have enough vouchers')}, status=status.HTTP_402_PAYMENT_REQUIRED)

        for p in pending_transactions:
            p.save()

        return Response(
            {
                'status': 'ok',
                'transactions': [VoucherUseLogSerializer(p).data for p in pending_transactions]
            }
        )


class WorkLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkLogSerializer
    queryset = WorkLog.objects.all()


class UseLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoucherUseLogSerializer
    queryset = VoucherUseLog.objects.all()
