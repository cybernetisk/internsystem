import django_filters
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import get_current_timezone

from core.models import Card
from voucher.models import UseLog, Wallet, WorkLog
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
    user = django_filters.CharFilter(name='wallet__user__username')
    semester = django_filters.CharFilter(name='wallet__semester')
    date_from = django_filters.MethodFilter(action='filter_date_from')
    date_to = django_filters.MethodFilter(action='filter_date_to')

    class Meta:
        model = UseLog
        fields = ['id', 'user', 'semester']

    def filter_date_from(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_spent', lte=False)

    def filter_date_to(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_spent', lte=True)


class WalletFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')
    card_number = django_filters.MethodFilter(action='filter_card_number')
    valid = django_filters.MethodFilter(action='filter_active')

    class Meta:
        model = Wallet
        fields = ['user', 'card_number', 'semester']

    def filter_card_number(self, queryset, value):
        cards = Card.objects.filter(card_number=value)
        if cards.exists():
            return queryset.filter(user=cards.first().user)
        return queryset.none()

    def filter_active(self, queryset, value):
        return queryset.filter(semester__in=get_valid_semesters())


class WorkLogFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='wallet__user__username')
    issuing_user = django_filters.CharFilter(name='issuing_user__username')
    semester = django_filters.CharFilter(name='wallet__semester')
    date_from = django_filters.MethodFilter(action='filter_date_from')
    date_to = django_filters.MethodFilter(action='filter_date_to')

    class Meta:
        model = WorkLog
        fields = ['id', 'user', 'issuing_user', 'semester']

    def filter_date_from(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_worked', lte=False)

    def filter_date_to(self, queryset, value):
        return apply_date_filter(queryset, value, 'date_worked', lte=True)
