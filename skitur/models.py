from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from skitur.fields import PhoneField

class Trip(models.Model):
    """
    """
    name = models.CharField('Trip name', max_length=128, null=False, blank=False)
    date = models.DateField('Start date of the trip', null=False, blank=False)
    places = models.PositiveSmallIntegerField('Number of places on the trip', null=False)
    description = models.TextField('Trip description. Used on the signup form.', null=False, blank=False)
    # TODO: Limit registration to either volunteers, members, or everyone

    class Meta:
        ordering = ['date', 'name']

    def __str__(self):
        return self.name

class Cabin(models.Model):
    """
    """
    trip = models.ForeignKey(Trip, related_name='cabins', null=False, blank=False)
    name = models.CharField('Cabin name', max_length=128, null=False, blank=False)
    beds = models.PositiveSmallIntegerField('Number of beds in the cabin', null=False)

    class Meta:
        ordering = ['trip', 'name']

    def __str__(self):
        return '%s – %s' % (self.trip, self.name)

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

    # Validators
    #phone_validator = RegexValidator(regex='^\+?[1-9]\d{1,14}$', message='Must be a valid E.164 phone number.')

    # Model fields
    trip = models.ForeignKey(Trip, related_name='participants', null=False, blank=False)
    user = models.ForeignKey(User, related_name='trip_participations', null=False, blank=False)
    cabin = models.ForeignKey(Cabin, related_name='participants', null=True, blank=True)
    has_payed = models.BooleanField('Payment has been received.', default=False, null=False)
    has_cancelled = models.BooleanField('Participant has cancelled the registration', default=False, null=False)
    notes = models.TextField(default='', null=False, blank=True)
    phone = PhoneField('Phone number', null=False, blank=False)#, validators=[phone_validator])
    registration_time = models.DateTimeField('Registration time', auto_now_add=True, null=False, blank=False)
    affiliation = models.CharField('Ifi affiliation', max_length=2, choices=AFFILIATION_CHOICES, default=NONE, null=False, blank=False)

    class Meta:
        ordering = ['trip', 'user']

    def __str__(self):
        return '%s – %s' % (self.trip, self.user)

class Wish(models.Model):
    """
    """
    participant = models.ForeignKey(Participant, related_name='wishes', null=False, blank=False)
    wish = models.ForeignKey(Participant, related_name='wished_by', null=False, blank=False)

    class Meta:
        ordering = ['participant', 'wish']
        verbose_name_plural = 'wishes'

    def __str__(self):
        return '%s – %s -> %s' % (self.participant.trip, self.participant.user, self.wish.user)
