from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from core.models import User


class Event(models.Model):
    """
    This is an event in the calendar. It can either be an all-day event or an
    event with a from and to timestamp.
    """

    # if is_allday is True: start and end should have correct expected naive date when formatted as UTC
    #                       (the time-details should be considered discarded)
    start = models.DateTimeField("Start time of the event", blank=False)
    end = models.DateTimeField("End time of the event", blank=False)

    is_allday = models.BooleanField("Is this an all-day event?", default=False)

    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    comment = models.TextField("Non-public comment", blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)

    organizer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    is_published = models.BooleanField(
        "Event is published (specially shown on intern, never public)", default=False
    )
    is_public = models.BooleanField(
        "Public (event will be visible on cyb.no)", default=False
    )
    is_external = models.BooleanField(
        "External event, not associated with CYB", default=False
    )
    in_escape = models.BooleanField("Occupies Escape", default=True)
    is_cancelled = models.BooleanField("Event has been cancelled", default=False)

    def clean(self):
        """
        This validates that the start time is before the end time
        """
        super(Event, self).clean()

        if self.start and self.end and self.end < self.start:
            raise ValidationError({"start": "Start time must be before end time"})

    def start_localtime(self):
        return timezone.localtime(self.start)

    def end_localtime(self):
        return timezone.localtime(self.end)

    def start_date(self):
        tz = timezone.utc if self.is_allday else None
        return timezone.localtime(self.start, tz).date()

    def end_date(self):
        tz = timezone.utc if self.is_allday else None
        return timezone.localtime(self.end, tz).date()

    def __str__(self):
        return "Event at %s: %s" % (self.start, self.title)
