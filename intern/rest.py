from rest_framework import viewsets

from intern.models import *
from intern.serializers import InternSerializer, InternGroupSerializer, AccessLevelSerializer


class InternViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Intern.objects.all()

    def get_serializer_class(self):
        return InternSerializer


class InternGroupViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return InternGroup.objects.all()

    def get_serializer_class(self):
        return InternGroupSerializer


class AccessLevelViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return AccessLevel.objects.all()

    def get_serializer_class(self):
        return AccessLevelSerializer
