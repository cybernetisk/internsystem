import datetime
from dateutil import parser
from collections import OrderedDict

from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from core.models import User, Semester
from core.utils import get_semester_of_date
from members.filters import MemberFilter
from members.models import Member, GeneralAssembly
from members.serializers import *

class GeneralAssemblyViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    queryset = GeneralAssembly.objects.all()

    def get_serializer_class(self):
        if self.action in ['list']:
            return GeneralAssemblySerializer
        elif self.action in ['create']:
            return AddGeneralAssemblySerializer
        return GeneralAssemblyFullSeralizer

    def create(self, request, *args, **kwargs):
        serializer = AddGeneralAssemblySerializer(data=request.data)
        serializer.is_valid()
        time = parser.parse(serializer.data['time'])
        semester = get_semester_of_date(time)

        generalassembly = GeneralAssembly(
            name=serializer.data['name'],
            time = time,
            semester=semester,
            extraordinary=serializer.data['extraordinary']
        )

        generalassembly.save()

        return Response(GeneralAssemblyFullSeralizer(generalassembly).data, status=status.HTTP_201_CREATED)

class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions,)
    filter_class = MemberFilter
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('lifetime',)
    search_fields = ('name',)
    ordering_fields = ('date_joined', 'name')

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddMemberSerializer
        return MemberSerializer

    def get_queryset(self):
        members = Member.objects.all()
        members = Member.objects.select_related('semester', 'seller', 'user')
        return members

    def create(self, request, **kwargs):
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.user
        adder = User.objects.get(username=id)
        semester = get_semester_of_date(datetime.datetime.now())
        lifetime = serializer.data['lifetime']
        try:
            user = User.objects.get(email=serializer.data['email'])
        except:
            user = None
        member = Member(
            seller=adder,
            last_edited_by=adder,
            semester=semester,
            name=serializer.data['name'],
            lifetime=serializer.data['lifetime'],
            email=serializer.data['email'],
            honorary=False,
        )
        if 'uio_username' in serializer.data:
            member.uio_username = serializer.data['uio_username']
        if user is not None:
            member.user = user
        if lifetime:
            member.date_lifetime = timezone.now()

        member.save()

        return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        member = self.get_object()

        member.name = request.data['name']
        member.email = request.data['email']
        member.last_edited_by = User.objects.get(username=request.user)
        lifetime = (request.data['lifetime'] == 'true')
        if lifetime and not member.lifetime:
            member.date_lifetime = timezone.now()
            member.lifetime = True
        elif (not lifetime) and member.lifetime:
            member.date_lifetime = None
            member.lifetime = False

        if 'honorary' in request.data:
            member.honorary = (request.data['honorary'] == 'true')
        if 'comments' in request.data:
            member.comments = request.data['comments']

        member.save()

        return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)


class MemberStatsViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        semesters = Semester.objects.all()
        semlist = OrderedDict()
        for semester in semesters:
            semlist[semester.id] = self.make_stats_dict(semester)

        serializers = MemberSemesterSerializer(semlist.values(), many=True)
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        semesters = Semester.objects.all()
        semester = get_object_or_404(semesters, pk=pk)
        serializer = MemberSemesterSerializer(self.make_stats_dict(semester))
        return Response(serializer.data)

    def make_stats_dict(self, semester):
        members = semester.member_set
        lifetime = members.filter(lifetime=True).count()
        honorary = members.filter(honorary=True).count()
        normal = members.filter(lifetime=False, honorary=False).count()
        semid = semester.id
        semdict = {
            'id': semid,
            'lifetime': lifetime,
            'honorary': honorary, 'normal': normal,
            'semester': semester}
        return semdict