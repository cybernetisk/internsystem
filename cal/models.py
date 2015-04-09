from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from cyb_oko.settings import TIME_ZONE


class Event(models.Model):
    """
    This is an event in the calendar. It can either be an all-day event or an
    event with a from and to timestamp.
    """

    start=models.DateTimeField('Start time of the event', null=False, blank=False)
    end=models.DateTimeField('End time of the event', null=False, blank=False)

    is_allday=models.BooleanField('Is this an all-day event?', null=False, default=False)

    title=models.CharField(max_length=128, null=False, blank=False)
    description=models.TextField(null=False, blank=True)

    is_public=models.BooleanField('Public (event will be visible on cyb.no)', null=False, default=False)
    is_rented=models.BooleanField('Rental', null=False, default=False)
    in_escape=models.BooleanField('In Escape', null=False, default=True)
    is_cancelled=models.BooleanField('Event has been cancelled', null=False, default=False)

    def clean(self):
        """
        This validates that the start time is before the end time
        """
        super(Event, self).clean()

        if self.start and self.end and self.end < self.start:
            raise ValidationError({'start': "Start time must be before end time"})

    def start_localtime(self):
        return timezone.localtime(self.start)

    def end_localtime(self):
        return timezone.localtime(self.end)

    def start_date(self):
        return timezone.localtime(self.start).date()

    def end_date(self):
        return timezone.localtime(self.end).date()


    def __str__(self):
        return 'Event at %s: %s' % (self.start, self.title)
