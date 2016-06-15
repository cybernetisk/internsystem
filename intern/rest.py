from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import DjangoModelPermissions
from intern.models import *
from intern.serializers import InternSerializer, InternRoleSerializer, InternGroupSerializer, AccessLevelSerializer


class InternViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    search_fields = ('name', 'roles')

    def get_queryset(self):
        return Intern.objects.all()

    def get_serializer_class(self):
        return InternSerializer


class InternGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        return InternGroup.objects.all()

    def get_serializer_class(self):
        return InternGroupSerializer


class AccessLevelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        return AccessLevel.objects.all()

    def get_serializer_class(self):
        return AccessLevelSerializer


class InternRoleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('groups',)

    def get_queryset(self):
        return InternRole.objects.all()

    def get_serializer_class(self):
        return InternRoleSerializer
