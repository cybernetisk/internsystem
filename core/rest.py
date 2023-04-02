from rest_framework import viewsets, filters, permissions
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from core.serializers import (
    CardCreateSerializer,
    CardSerializer,
    UserExtendedSerializer,
    NfcCardCreateSerializer,
    NfcCardSerializer,
    GroupSerializer,
)
from core.models import Card, User, NfcCard, Group
from core.filters import CardFilter, UserFilter, NfcCardFilter
from core.permissions import CardPermission


class CardViewSet(viewsets.ModelViewSet):
    permission_classes = (CardPermission,)
    filterset_class = CardFilter
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    queryset = Card.objects.all()
    ordering_fields = ("id", "user__username", "card_number", "disabled")
    filterset_fields = ("id", "user__id", "card_number", "user__intern__id")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CardCreateSerializer
        return CardSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=serializer.data["user"])
        if user != request.user:
            if not request.user.has_perm(
                "%s.add_%s" % (Card._meta.app_label, Card._meta.model_name)
            ):
                self.permission_denied(request)

        card = Card(user=user, card_number=serializer.data["card_number"])
        card.save()
        return Response(CardSerializer(card).data, status=status.HTTP_201_CREATED)

    def destroy(self, request):
        instance = self.get_object()

        if instance.user != request.user:
            if not request.user.has_perm(
                "%s.delete_%s" % (Card._meta.app_label, Card._meta.model_name)
            ):
                self.permission_denied(request)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NfcCardViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    filterset_class = NfcCardFilter
    queryset = NfcCard.objects.all()
    ordering_fields = ("card_uid", "user", "intern")

    def get_serializer_class(self):
        if self.action in ["create"]:
            return NfcCardCreateSerializer
        return NfcCardSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = None
        # A NFC card does not need a user. Omitting this will cause a 500 if no user is supplied.
        if serializer.data["user"]:
            user = User.objects.get(id=serializer.data["user"])
        if user != request.user:
            if not request.user.has_perm(
                "%s.add_%s" % (Card._meta.app_label, Card._meta.model_name)
            ):
                self.permission_denied(request)

        card = serializer.save()
        return Response(NfcCardSerializer(card).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = UserFilter
    search_fields = ("username", "realname", "email")
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all().order_by("username")
    lookup_field = "username"

    def get_serializer_class(self):
        return UserExtendedSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
