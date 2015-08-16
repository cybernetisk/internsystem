import django_filters
from rest_framework import viewsets
from rest_framework import filters

from cal.serializers import *
from cal.models import Event


class EventFilter(django_filters.FilterSet):
    f = django_filters.DateFilter(name='end', lookup_type='gte')
    t = django_filters.DateFilter(name='start', lookup_type='lte')

    class Meta:
        model = Event
        fields = ('id', 'start', 'end', 'is_allday', 'title',
                  'is_published', 'is_public', 'is_external', 'in_escape', 'is_cancelled', 'f', 't')


class EventViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = EventFilter
    search_fields = ('title',)

    def get_queryset(self):
        queryset = Event.objects.all().order_by('start')

        if 'show_cancelled' not in self.request.query_params:
            queryset = queryset.filter(is_cancelled=False)

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_authenticated():
            if self.action in ['create', 'update']:
                return EventWriteSerializer
            return EventSerializer
        return EventGuestSerializer
