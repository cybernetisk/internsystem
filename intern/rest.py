from rest_framework import viewsets

from intern.models import *
from intern.serializers import InternSerializer


class InternViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Intern.objects.all()

    def get_serializer_class(self):
        return InternSerializer
