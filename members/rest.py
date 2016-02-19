import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from rest_framework import filters

from members.serializers import *
from members.filters import MemberFilter
from members.permissions import MemberPermissions
from core.models import User
from core.utils import get_semester_of_date


class MemberViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, MemberPermissions)
    filter_class = MemberFilter
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    ordering_fields = ('date_joined', 'name')


    def get_serializer_class(self):
        if self.action in ['create']:
            return AddMemberSerializer
        return MemberSerializer

    def get_queryset(self):
        return Member.objects.filter(Q(semester=get_semester_of_date(datetime.datetime.now())) |
                                     Q(lifetime=True) | Q(honorary=True))

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
            semester=semester,
            name=serializer.data['name'],
            lifetime=serializer.data['lifetime'],
            email=serializer.data['email'],
            honorary=False,
            uio_username=serializer.data['uio_username']
        )
        if user is not None:
            member.user = user
        if lifetime:
            member.date_lifetime = datetime.datetime.now()

        member.save()

        return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)