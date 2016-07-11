import django_filters
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import get_current_timezone

from core.models import NfcCard
from voucher.models import UseLog, Wallet, WorkLog, VoucherWallet, CoffeeWallet, VoucherUseLog, CoffeeUseLog, \
    CoffeeRegisterLog
from voucher.utils import get_valid_semesters


def apply_date_filter(queryset, value, field, lte):
    try:
        t = datetime.strptime(value, '%Y-%m-%d').replace(tzinfo=get_current_timezone())
        field += '__lte' if lte else '__gte'
        if lte:
            t += timedelta(days=1)
        return queryset.filter(**{field: t})
    except ValueError:
        raise ValidationError(detail=_('Date format of %(date)s not recognized') % {'date': value})


class UseLogFilter(django_filters.FilterSet):
    semester = django_filters.CharFilter(name='wallet__semester')
    date_from = django_filters.MethodFilter(action='filter_date_from')
    date_to = django_filters.MethodFilter(action='filter_date_to')

    def filter_date_from(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_spent', lte=False)

    def filter_date_to(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_spent', lte=True)


class VoucherUseLogFilter(UseLogFilter):
    user = django_filters.CharFilter(name='wallet__user__username')

    class Meta:
        model = VoucherUseLog
        fields = ['id', 'user', 'semester']


class CoffeeUseLogFilter(UseLogFilter):
    card = django_filters.CharFilter(name='wallet__card__card_uid')

    class Meta:
        model = CoffeeUseLog
        fields = ['id', 'card', 'semester']


class WalletFilter(django_filters.FilterSet):
    valid = django_filters.MethodFilter(action='filter_active')

    class Meta:
        model = Wallet
        fields = ['semester']

    def filter_active(self, queryset, value):
        return queryset.filter(semester__in=get_valid_semesters())


class VoucherWalletFilter(WalletFilter):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = VoucherWallet
        fields = ['user', 'semester']


class CoffeeWalletFilter(WalletFilter):
    card = django_filters.CharFilter(name='nfccard__card_uid')

    class Meta:
        model = CoffeeWallet
        fields = ['card', 'semester']


class RegisterLogFilter(django_filters.FilterSet):
    issuing_user = django_filters.CharFilter(name='issuing_user__username')
    semester = django_filters.CharFilter(name='wallet__semester')


class CoffeeRegisterLogFilter(RegisterLogFilter):
    card = django_filters.CharFilter(name='wallet__card__card_uid')

    class Meta:
        model = CoffeeRegisterLog
        fields = ['id', 'card', 'issuing_user', 'semester']


class WorkLogFilter(RegisterLogFilter):
    user = django_filters.CharFilter(name='wallet__user__username')
    date_from = django_filters.MethodFilter(action='filter_date_from')
    date_to = django_filters.MethodFilter(action='filter_date_to')

    class Meta:
        model = WorkLog
        fields = ['id', 'user', 'issuing_user', 'semester']

    def filter_date_from(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_worked', lte=False)

    def filter_date_to(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_worked', lte=True)
