import django_filters
from rest_framework import viewsets, filters, permissions
from core.serializers import UserExtendedSerializer
from core.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email',
                  'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = UserFilter
    search_fields = ('username','realname','email')
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all().order_by('username')
    lookup_field = 'username'

    def get_serializer_class(self):
        return UserExtendedSerializer
