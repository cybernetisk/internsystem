import django_filters
from voucher.models import UseLog, WorkLog


class UseLogFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='wallet__user__username')
    semester = django_filters.CharFilter(name='wallet__semester')

    class Meta:
        model = UseLog
        fields = ['id', 'user', 'semester']


class WorkLogFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='wallet__user__username')
    issuing_user = django_filters.CharFilter(name='issuing_user__username')
    semester = django_filters.CharFilter(name='wallet__semester')

    class Meta:
        model = WorkLog
        fields = ['id', 'user', 'issuing_user', 'semester']
