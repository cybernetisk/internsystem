import datetime
from zoneinfo import ZoneInfo

import dateutil.rrule
import requests
from django.conf import settings
from django.core.cache import cache
from icalendar import Calendar
from icalendar import Event as CalEvent
from rest_framework import viewsets
from rest_framework.response import Response


class UpcomingRemoteEventViewSet(viewsets.ViewSet):
    _calendars = settings.CYB["CALENDAR"]

    def _get_time(self, dt):
        if type(dt) == datetime.date:
            return dt
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            # assume this timezone
            return dt.replace(tzinfo=ZoneInfo("Europe/Oslo"))
        return dt.astimezone(ZoneInfo("Europe/Oslo"))

    def _force_naive_datetime(self, dt):
        if type(dt) == datetime.date:
            dt = datetime.datetime.combine(dt, datetime.time.min)
        return dt.replace(tzinfo=None)

    def _get_rruleset(self, component):
        rruleset = dateutil.rrule.rruleset()

        # because dateutil.rrule don't adjust timezone offset, we handle
        # all dates and times in naive format and add timezone again later
        dtstart = self._force_naive_datetime(self._get_time(component["DTSTART"].dt))

        # handle recurrences
        rrulestr = component["RRULE"].to_ical().decode("utf-8")
        rrule = dateutil.rrule.rrulestr(rrulestr, dtstart=dtstart, ignoretz=True)
        rruleset.rrule(rrule)

        # handle exclusions
        if "EXDATE" in component:
            # the value here will be a list if it has multiple EXDATE occurences
            exdate_list = (
                [component["EXDATE"]]
                if not isinstance(component["EXDATE"], list)
                else component["EXDATE"]
            )
            for exdate in exdate_list:
                for d in exdate.dts:
                    rruleset.exdate(self._force_naive_datetime(self._get_time(d.dt)))

        return rruleset

    def _get_recurrences(self, component, recurrences_to_skip):
        rruleset = self._get_rruleset(component)
        is_day = type(component["DTSTART"].dt) == datetime.date

        latest_event_time = datetime.datetime.now() + datetime.timedelta(days=365)

        for d in rruleset:
            # limit recurring rules without end dates
            # (we expect not to show events more than one year in the future)
            if d > latest_event_time:
                break

            # the rrule parsing don't respect dst, so by removing timezone and adding it again
            # it will receive the correct timezone
            d = d.replace(tzinfo=None).replace(tzinfo=ZoneInfo("Europe/Oslo"))

            if is_day:
                d = d.date()

            # check if this has a single event that overrides the recurrence
            if d in recurrences_to_skip:
                continue

            yield d

    def _parse_summary(self, component):
        """
        Remove description from summary so only the title is left
        """
        summary = component["SUMMARY"]

        if "DESCRIPTION" in component and len(component["DESCRIPTION"]) > 0:
            pos = summary.find(": " + component["DESCRIPTION"][0:10])
            if pos != -1:
                summary = summary[0:pos]

        return summary

    def _parse_ics(self, ics_data):
        events = []

        ical_list = Calendar.from_ical(ics_data)
        recurrence_ids = []

        # build list of all future events, only non-recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or "RRULE" in component:
                continue

            if "RECURRENCE-ID" in component:
                recurrence_ids.append(component["RECURRENCE-ID"].dt)

            is_day = type(component["DTSTART"].dt) == datetime.date
            dtend = component["DTEND"].dt
            if is_day:
                # the ics format uses the following day for end when it is only one day
                # but we change it to be the same day for convenience
                dtend = dtend - datetime.timedelta(days=1)

            events.append(
                {
                    "all_day": is_day,
                    "start": self._get_time(component["DTSTART"].dt),
                    "end": self._get_time(dtend),
                    "summary": self._parse_summary(component),
                    "url": component["URL"] if "URL" in component else None,
                }
            )

        # build list of all future events, only recurring
        for component in ical_list.walk():
            if type(component) != CalEvent or "RRULE" not in component:
                continue

            is_day = type(component["DTSTART"].dt) == datetime.date
            duration = component["DTEND"].dt - component["DTSTART"].dt

            for d in self._get_recurrences(component, recurrence_ids):
                dtend = d + duration

                if is_day:
                    # the ics format uses the following day for end when it is only one day
                    # but we change it to be the same day for convenience
                    dtend = dtend - datetime.timedelta(days=1)

                events.append(
                    {
                        "all_day": is_day,
                        "start": d,
                        "end": dtend,
                        "summary": self._parse_summary(component),
                        "url": component["URL"] if "URL" in component else None,
                    }
                )

        return events

    def _update_confluence_cache(self):
        data = {}

        for calendar in self._calendars:
            events = []

            for url in self._calendars[calendar]:
                # TODO: failure handling
                r = requests.get(url)
                events += self._parse_ics(r.text)

            data[calendar] = events

        cache.set("cal_remote_events", data, 3000)
        return data

    def _get_data(self, use_cache=True):
        data = None
        if use_cache:
            data = cache.get("cal_remote_events")
        if data is None:
            data = self._update_confluence_cache()
        return data

    def list(self, request):
        cached = "nocache" not in request.GET

        if cached:
            out = cache.get("cal_remote_response")
            if out is not None:
                return Response(out)

        out = {}
        data = self._get_data(use_cache=cached)
        now = datetime.datetime.now(datetime.timezone.utc)
        osl = ZoneInfo("Europe/Oslo")

        def get_aware_date(dt):
            if type(dt) is datetime.date:
                dt = datetime.datetime.combine(dt, datetime.time.min)
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                dt = dt.replace(tzinfo=osl)
            return dt

        def is_future(ev):
            end = get_aware_date(ev["end"])
            if ev["all_day"]:
                end += datetime.timedelta(days=1)
            return end > now

        def get_start_time(ev):
            return get_aware_date(ev["start"])

        for calendar in self._calendars:
            events = data[calendar]
            events = filter(is_future, events)
            events = sorted(events, key=get_start_time)[:15]
            out[calendar] = events

        cache.set("cal_remote_response", out, 600)
        return Response(out)
