import django_filters
from rest_framework.response import Response
from rest_framework import viewsets, filters

from cal.serializers import *
from cal.models import Event
from core.serializers import SemesterSerializer
from core.models import Semester
from core.utils import get_semester_details_from_date


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


class SemesterViewSet(viewsets.ViewSet):
    def list(self, request):
        # TODO: this method should probably be optimized

        semesters_simple = []
        for field in ('start', 'end'):
            for date in Event.objects.datetimes(field, 'month'):
                semester = get_semester_details_from_date(date)
                if semester not in semesters_simple:
                    semesters_simple.append(semester)

        semesters_models = []
        semesters_cache = Semester.objects.all()
        for item in semesters_simple:
            found = False
            for cache_item in semesters_cache:
                if cache_item.year == item['year'] and cache_item.semester == item['semester']:
                    semesters_models.append(cache_item)
                    found = True
                    break

            if not found:
                obj, created = Semester.objects.get_or_create(year=item['year'], semester=item['semester'])
                semesters_models.append(obj)

        serializer = SemesterSerializer(semesters_models, many=True)
        return Response(serializer.data)
