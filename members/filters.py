import django_filters

from django.db.models import Q
from members.models import Member
import datetime
from core.utils import get_semester_of_date

class MemberFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = Member
        fields = ['name', 'email', 'semester', 'lifetime', 'honorary']
