from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from members.serializers import *
from core.models import User
from core.utils import get_semester_of_date
import datetime


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ['create']:
            return AddMemberSerializer
        return MemberSerializer

    def create(self, request, **kwargs):
        serializer = AddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = request.user
        adder = User.objects.get(username=id)
        date_joined = datetime.datetime.now()
        semester = get_semester_of_date(date_joined)
        try:
            user = User.objects.get(email=serializer.data['email'])
        except:
            user = None
        member = Member(
            seller=adder,
            date_joined=date_joined,
            semester=semester,
            name=serializer.data['name'],
            lifetime=serializer.data['lifetime'],
            email=serializer.data['email'],
            honorary=False
        )
        if user is not None:
            member.user = user
        member.save()

        return Response(MemberSerializer(member).data, status=status.HTTP_201_CREATED)




    def list(self, request, username=None):
        objects = Member.objects.filter(Q(semester=get_semester_of_date(datetime.datetime.now())) |
                                        Q(lifetime=True) | Q(honorary=True))
        serializers = MemberSerializer(objects, many=True)

        return Response(serializers.data)