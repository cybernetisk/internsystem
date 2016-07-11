# from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as _UserManager

from django.core.mail import send_mail
from django.core import validators
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(_UserManager):
    pass


class User(AbstractBaseUser, PermissionsMixin):
    """
    The user model we use instead of User model provided by Django.
    Based on Django's User model.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, digits and '
                                            '@/./+/-/_ only.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
                                ])
    realname = models.CharField(_('real name'), max_length=60, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = PhoneNumberField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # TODO: ModelAdmin for this custom thing
    # see https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#custom-users-and-django-contrib-admin

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        "Returns the full name for the user."
        return self.realname

    def get_short_name(self):
        "Returns the short name for the user."
        return self.realname

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Semester(models.Model):
    SPRING = '1-SPRING'  # number prefixed for easier sorting
    FALL = '2-FALL'
    SEM_CHOICES = (
        (SPRING, 'Vår'),
        (FALL, 'Høst')
    )

    semester = models.CharField(max_length=8, choices=SEM_CHOICES)
    year = models.SmallIntegerField()

    def __str__(self):
        return self.get_semester_display() + " " + str(self.year)

    class Meta:
        ordering = ['-year', '-semester']
        unique_together = ("semester", "year")


class Card(models.Model):
    CARD_NUMBER_REGEX = r'^\d{6}\.\d{2}\.\d{7}(\.\d)?$'
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=20, blank=True)
    disabled = models.BooleanField(default=False)
    card_number = models.CharField(max_length=20, unique=True,
                                   validators=[
                                       validators.RegexValidator(CARD_NUMBER_REGEX, _('Enter a valid card number.'),
                                                                 'invalid')
                                   ])

    def __str__(self):
        return "%s - %s (%s)" % (self.user.username, self.card_number, self.comment)


class NfcCard(models.Model):
    CARD_UID_REGEX = r'^[a-z0-9]{8}$'

    card_uid = models.CharField(unique=True, max_length=8,
                                validators=[
                                    validators.RegexValidator(CARD_UID_REGEX, _('Enter valid card uid.'), 'invalid')
                                ])
    user = models.ForeignKey(User, blank=True, null=True)
    intern = models.BooleanField(default=False)
    comment = models.CharField(max_length=20, blank=True)

    def __str__(self):
        if not self.user:
            return self.card_uid
        return "%s (%s)" % (self.card_uid, self.user)
