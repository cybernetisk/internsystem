from rest_framework import viewsets
from rest_framework.response import Response

from members.serializers import *


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, username=None):
        adder = self.get_object()
        return Response(self.serializer_class)


    def list(self, request, username=None):
        objects = Member.objects.all()
        serializers = MemberSerializer(objects, many=True)
        return Response(serializers.data)