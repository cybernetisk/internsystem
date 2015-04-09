from rest_framework import viewsets
from rest_framework import filters

from cal.serializers import EventSerializer
from cal.models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
