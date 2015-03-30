from django.db import models
from django.contrib.auth.models import User

class Trip(models.Model):
    """
    """
    date = models.DateField('Start date of the trip', null=False, blank=False)
    places = models.PositiveSmallIntegerField('Number of places on the trip', null=False)
    description = models.TextField('Trip description. Used on the signup form.', null=False, blank=False)
    # TODO: Limit registration to either volunteers, members, or everyone

class Cabin(models.Model):
    """
    """
    trip = models.ForeignKey(Trip, related_name='cabins', null=False)
    name = models.CharField('Cabin name', max_length=128, null=False, blank=False)
    beds = models.PositiveSmallIntegerField('Number of beds in the cabin', null=False)

class Participant(models.Model):
    """
    """
    STUDENT = 'ST'
    ALUMNUS = 'AL'
    NONE = 'NO'

    AFFILIATION_CHOICES = (
            (STUDENT, 'Student'),
            (ALUMNUS, 'Alumnus'),
            (NONE, 'None')
    )

    user = models.ForeignKey(User, related_name='trip_participations', null=False)
    cabin = models.ForeignKey(Cabin, related_name='participants', null=True)
    has_payed = models.BooleanField('Payment has been received.', default=False)
    has_cancelled = models.BooleanField('Participant has cancelled the registration', default=False)
    notes = models.TextField(default='', null=False, blank=True)
    phone = models.CharField('Phone number', max_length=16, null=False, blank=False)
    registration_time = models.DateTimeField('Registration time', auto_now_add=True, null=False, blank=False)
    affiliation = models.CharField('Ifi affiliation', max_length=2, choices=AFFILIATION_CHOICES, default=NONE, null=False, blank=False)

class Wish(models.Model):
    """
    """
    participant = models.ForeignKey(Participant, related_name='wishes', null=False)
    wish = models.ForeignKey(Participant, related_name='wished_by', null=False)
