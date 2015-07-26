from rest_framework import viewsets
from rest_framework import filters

from cal.serializers import *
from cal.models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            if self.action in ['create', 'update']:
                return EventWriteSerializer
            return EventSerializer
        return EventGuestSerializer
