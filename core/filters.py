import django_filters
from core.models import Card, User, NfcCard


class CardFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = Card
        fields = ['user', 'card_number', 'disabled']


class NfcCardFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name='user__username')

    class Meta:
        model = NfcCard
        fields = ['card_uid', 'user', 'intern']


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email',
                  'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')
