import django_filters

from members.models import Member


class MemberFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = Member
        fields = ['name', 'email', 'semester', 'lifetime', 'honorary']
