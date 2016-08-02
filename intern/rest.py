from django.utils import timezone
from django.db import IntegrityError

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.utils import get_semester

from intern.models import *
from intern.serializers import InternRoleFullSerializer, InternSerializer, AccessLevelSerializer, InternGroupSerializer, \
    RoleSerializer, AddInternRoleSerializer, InternCardSerializer, AddInternCardSerializer


class InternViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    search_fields = ('user__username',)
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)
    filter_fields = ('user', 'user__username')
    serializer_class = InternSerializer
    queryset = Intern.objects.all()


class InternGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = InternGroupSerializer
    queryset = InternGroup.objects.all()


class AccessLevelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    serializer_class = AccessLevelSerializer
    queryset = AccessLevel.objects.all()


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('groups',)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class InternCardViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_field = ('intern', 'semester')
    ordering_fields = ('intern',)
    queryset = InternCard.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddInternCardSerializer
        return InternCardSerializer


class InternRoleViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('intern', 'role', 'semesters',
                     'role__groups', 'role__id')
    search_fields = ('intern', 'role')
    ordering_fields = ('intern',)

    def get_queryset(self):
        return InternRole.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddInternRoleSerializer
        return InternRoleFullSerializer

    def create(self, request, *args, **kwargs):
        serializer = AddInternRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']

        user = User.objects.get_or_create(username=username)[0]
        intern = Intern.objects.get_or_create(user=user)[0]
        role = Role.objects.get(pk=serializer.data['role'])

        internrole = InternRole.objects.get_or_create(intern=intern, role=role)[0]
        creator = User.objects.get(username=request.user)

        # if the user have been active before we remove the old date_removed and add a comment
        if internrole.date_removed is not None:
            internrole.date_removed = None
            internrole.removed_by = None
            internrole.comments = ' %s\nRecreated by %s' % (internrole.comments, creator)
        else:
            internrole.created_by = creator

        internrole.last_editor = creator
        intern.update_left()
        internrole.semesters.add(get_semester())

        try:
            internrole.save()
        except IntegrityError:
            return Response(
                {'error': ('Error when adding internrole: %s %s. It already exist' % (role.name, user.username))
                 }, status=status.HTTP_406_NOT_ACCEPTABLE
            )

        return Response(InternRoleFullSerializer(internrole).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        internrole = self.get_object()
        internrole.last_editor = User.objects.get(username=request.user)
        internrole.date_edited = timezone.now().date()
        internrole.comments = '%s\n%s' % (internrole.comments, serializer.data['comments'])
        internrole.recieved_interncard = serializer.data['recieved_interncard']

        if serializer.data['access_given'] and internrole.access_given == False:
            internrole.access_given = True
            internrole.date_access_given = timezone.now()
            internrole.date_access_revoked = None
            internrole.comments = '%s\n%s gave access for role %s' % (
                internrole.comments, internrole.last_editor, internrole.role)

        if serializer.data['access_given'] is False and internrole.access_given is True:
            internrole.access_given = False
            internrole.date_access_revoked = timezone.now()
            internrole.comments = '%s\n%s revoked access for role %s' % (
                internrole.comments, internrole.last_editor, internrole.role)

        internrole.save()

        return Response(InternRoleFullSerializer(internrole).data, status=status.HTTP_200_OK)


def destroy(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    internrole = self.get_object()
    internrole.date_removed = timezone.now()
    internrole.removed_by = User.objects.get(username=request.user)
    internrole.comments = '%s\nRemoved by: %s' % (internrole.comments, internrole.removed_by)
    internrole.save()

    internrole.intern.update_left()

    return Response(InternRoleFullSerializer(internrole).data, status=status.HTTP_200_OK)
