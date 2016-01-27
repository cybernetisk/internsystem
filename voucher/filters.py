import django_filters

from core.models import Card
from voucher.models import UseLog, Wallet, WorkLog
from voucher.utils import get_valid_semesters


class UseLogFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='wallet__user__username')
    semester = django_filters.CharFilter(name='wallet__semester')

    class Meta:
        model = UseLog
        fields = ['id', 'user', 'semester']


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

    class Meta:
        model = WorkLog
        fields = ['id', 'user', 'issuing_user', 'semester']
