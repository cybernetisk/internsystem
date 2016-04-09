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

    def _get_time(self, dt):
        if type(dt) == datetime.date:
            return dt
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            # assume this timezone
            return dt.replace(tzinfo=pytz.timezone("Europe/Oslo"))
        return dt.astimezone(pytz.timezone("Europe/Oslo"))

    def _force_naive_datetime(self, dt):
        if type(dt) == datetime.date:
            dt = datetime.datetime.combine(dt, datetime.time.min)
        return dt.replace(tzinfo=None)

    def _get_rruleset(self, component):
        rruleset = dateutil.rrule.rruleset()

        # because dateutil.rrule don't adjust timezone offset, we handle
        # all dates and times in naive format and add timezone again later
        dtstart = self._force_naive_datetime(self._get_time(component['DTSTART'].dt))

        # handle recurrences
        rrulestr = component['RRULE'].to_ical().decode('utf-8')
        rrule = dateutil.rrule.rrulestr(rrulestr, dtstart=dtstart, ignoretz=True)
        rruleset.rrule(rrule)

        # handle exclusions
        if 'EXDATE' in component:
            for exdate in component['EXDATE'].dts:
                rruleset.exdate(self._force_naive_datetime(self._get_time(exdate.dt)))

        return rruleset

    def _get_recurrences(self, component, recurrences_to_skip):
        rruleset = self._get_rruleset(component)
        is_day = type(component['DTSTART'].dt) == datetime.date

        for d in rruleset:
            # the rrule parsing don't respect dst, so by removing timezone and adding it again
            # it will receive the correct timezone
            d = pytz.timezone("Europe/Oslo").localize(d.replace(tzinfo=None))

            if is_day:
                d = d.date()

            # check if this has a single event that overrides the recurrence
            if d in recurrences_to_skip:
                continue

            yield d

    def _parse_ics(self, ics_data):
        events = []

        ical_list = Calendar.from_ical(ics_data)
        recurrence_ids = []

        # build list of all future events, only non-recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or 'RRULE' in component:
                continue

            if 'RECURRENCE-ID' in component:
                recurrence_ids.append(component['RECURRENCE-ID'].dt)

            is_day = type(component['DTSTART'].dt) == datetime.date
            dtend = component['DTEND'].dt
            if is_day:
                # the ics format uses the following day for end when it is only one day
                # but we change it to be the same day for convenience
                dtend = dtend - datetime.timedelta(days=1)

            events.append({
                'all_day': is_day,
                'start': self._get_time(component['DTSTART'].dt),
                'end': self._get_time(dtend),
                'summary': component['SUMMARY'],
                'url': component['URL'] if 'URL' in component else None
            })

        # build list of all future events, only recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or 'RRULE' not in component:
                continue

            is_day = type(component['DTSTART'].dt) == datetime.date
            duration = component['DTEND'].dt - component['DTSTART'].dt

            for d in self._get_recurrences(component, recurrence_ids):
                dtend = d + duration

                if is_day:
                    # the ics format uses the following day for end when it is only one day
                    # but we change it to be the same day for convenience
                    dtend = dtend - datetime.timedelta(days=1)

                events.append({
                    'all_day': is_day,
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

    def _get_data(self, use_cache=True):
        data = None
        if use_cache:
            data = cache.get('cal_remote_events')
        if data is None:
            data = self._update_cache()
        return data

    def list(self, request):
        out = {}
        data = self._get_data(use_cache='nocache' not in request.GET)
        now = datetime.datetime.now(pytz.utc)
        osl = pytz.timezone("Europe/Oslo")

        def is_future(ev):
            end = datetime.datetime.combine(ev['end'], datetime.time.min).replace(tzinfo=osl)
            if ev['all_day']:
                end += datetime.timedelta(days=1)
            return end > now

        def get_start_time(ev):
            return datetime.datetime.combine(ev['start'], datetime.time.min).replace(tzinfo=osl)

        for calendar in self._calendars:
            events = data[calendar]
            events = filter(is_future, events)
            events = sorted(events, key=get_start_time)[:15]
            out[calendar] = events

        return Response(out)
