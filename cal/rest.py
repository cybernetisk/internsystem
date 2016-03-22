import django_filters
from rest_framework.response import Response
from rest_framework import viewsets, filters, renderers

from cal.renderers import IcsRenderer
from cal.serializers import *
from cal.models import Event
from core.serializers import SemesterSerializer
from core.models import Semester
from core.utils import get_semester_details_from_date

import requests
import dateutil.rrule
import datetime
import pytz
from icalendar import Calendar, Event as CalEvent
from django.core.cache import cache


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
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        IcsRenderer,
    )

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

    def retrieve(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'ics':
            return Response([self.get_object()])

        return super(EventViewSet, self).retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if request.accepted_renderer.format == 'ics':
            queryset = self.filter_queryset(self.get_queryset())
            return Response(queryset)

        return super(EventViewSet, self).list(request, *args, **kwargs)


class EscapeOccupiedViewSet(viewsets.GenericViewSet):
    queryset = Event.objects.filter(is_cancelled=False, in_escape=True).order_by('start')

    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter

    serializer_class = EscapeOccupiedEventSerializer

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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


class UpcomingRemoteEventViewSet(viewsets.ViewSet):
    _calendars = {
        'intern': [
            'https://confluence.cyb.no/rest/calendar-services/1.0/calendar/export/subcalendar/private/4f5af3ae5b9a67666c2ad001d21c7c453291844a.ics'
        ],
        'public': [
            'https://confluence.cyb.no/rest/calendar-services/1.0/calendar/export/subcalendar/private/69e4d3450b6ba6e4a547882144bdedfc5182c40a.ics'
        ]
    }

    def _parse_ics(self, ics_data):
        events = []

        ical_list = Calendar.from_ical(ics_data)
        now = datetime.datetime.now(pytz.utc)

        recurrenceIds = []

        # build list of all future events, only non-recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or 'RRULE' in component:
                continue

            # if component['DTEND'].dt <= now:
            #    continue

            if 'RECURRENCE-ID' in component:
                recurrenceIds.append(component['RECURRENCE-ID'].dt)

            events.append({
                'start': component['DTSTART'].dt,
                'end': component['DTEND'].dt,
                'summary': component['SUMMARY'],
                'url': component['URL'] if 'URL' in component else None
            })

        # build list of all future events, only recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or 'RRULE' not in component:
                continue

            dtstart = component['DTSTART'].dt.astimezone(pytz.timezone("Europe/Oslo"))
            duration = component['DTEND'].dt - component['DTSTART'].dt
            rrulestr = component['RRULE'].to_ical().decode('utf-8')
            rrule = dateutil.rrule.rrulestr(rrulestr, dtstart=dtstart)

            for d in rrule:
                # the rrule parsing don't respect dst, so by removing timezone and adding it again
                # it will receive the correct timezone
                d = pytz.timezone("Europe/Oslo").localize(d.replace(tzinfo=None))
                dtend = d + duration
                if d not in recurrenceIds:
                    events.append({
                        'start': d,
                        'end': dtend,
                        'summary': component['SUMMARY'],
                        'url': component['URL'] if 'URL' in component else None
                    })

        return events

    def _update_cache(self):
        data = {}

        for calendar in self._calendars:
            events = []

            for url in self._calendars[calendar]:
                # TODO: failure handling
                r = requests.get(url)
                events += self._parse_ics(r.text)

            data[calendar] = events

        cache.set('cal_remote_events', data, 300)
        return data

    def _get_data(self):
        data = cache.get('cal_remote_events')
        if data is None:
            data = self._update_cache()
        return data

    def list(self, request):
        out = {}
        data = self._get_data()
        now = datetime.datetime.now(pytz.utc)
        osl = pytz.timezone("Europe/Oslo")

        def is_future(ev):
            # TODO: improve this forcing it to be aware datetime object
            return datetime.datetime.combine(ev['end'], datetime.time.min).replace(tzinfo=osl) > now

        def get_start_time(ev):
            # TODO: improve this forcing it to be aware datetime object
            return datetime.datetime.combine(ev['start'], datetime.time.min).replace(tzinfo=osl)

        for calendar in self._calendars:
            events = data[calendar]
            events = filter(is_future, events)
            events = sorted(events, key=get_start_time)[:15]
            out[calendar] = events

        return Response(out)
