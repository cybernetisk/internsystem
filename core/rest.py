from rest_framework import viewsets, filters, permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import CardCreateSerializer, CardSerializer, UserExtendedSerializer
from core.models import Card, User
from core.filters import CardFilter, UserFilter


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_class = CardFilter
    queryset = Card.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return CardCreateSerializer
        return CardSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=serializer.data['user'])
        if user != request.user:
            if not request.user.has_perm('%s.add_%s' % (Card._meta.app_label, Card._meta.model_name)):
                self.permission_denied(request)

        card = serializer.save()
        return Response(CardSerializer(card).data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        instance = self.get_object()

        if instance.user != request.user:
            if not request.user.has_perm('%s.delete_%s' % (Card._meta.app_label, Card._meta.model_name)):
                self.permission_denied(request)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = UserFilter
    search_fields = ('username', 'realname', 'email')
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all().order_by('username')
    lookup_field = 'username'

    def get_serializer_class(self):
        return UserExtendedSerializer
