import django_filters
import datetime
from django.db.models import Q

from core.utils import get_semester_of_date
from members.models import Member


class MemberFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')
    valid = django_filters.Filter(method='filter_valid')

    def filter_valid(self, queryset, name, value):
        return queryset.filter(Q(semester=get_semester_of_date(datetime.datetime.now())) |
                              Q(lifetime=True) | Q(honorary=True))

    class Meta:
        model = Member
        fields = ['name', 'email', 'semester', 'lifetime', 'honorary']
