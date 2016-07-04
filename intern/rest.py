from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from intern.models import *
from intern.serializers import InternRoleFullSerializer, InternSerializer, AccessLevelSerializer, InternGroupSerializer, \
    RoleSerializer, AddInternRoleSerializer


class InternViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    search_fields = ('user__username', 'user__realname')
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_fields = ('user', 'user__username')

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


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('groups',)

    def get_queryset(self):
        return Role.objects.all()

    def get_serializer_class(self):
        return RoleSerializer


class InternRoleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('intern', 'role', 'semester_start', 'semester_end',
                     'role__groups', 'role__id')
    search_fields = ('intern', 'role')

    def get_queryset(self):
        return InternRole.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddInternRoleSerializer
        return InternRoleFullSerializer
