from django.db import models, transaction
from django.db.models import Sum
from core.models import User, Card, Semester
from decimal import Decimal

import calendar
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Wallet(models.Model):
    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    cached_balance = models.DecimalField(default=0, max_digits=8, decimal_places=2, editable=False)

    class Meta:
        unique_together = ("user", "semester")

    def calculate_balance(self):
        vouchers_earned = WorkLog.objects.filter(wallet=self).aggregate(sum=Sum('vouchers'))['sum'] or Decimal(0)
        vouchers_used = UseLog.objects.filter(wallet=self).aggregate(sum=Sum('vouchers'))['sum'] or Decimal(0)
        self.cached_balance = vouchers_earned - vouchers_used
        self.save()
        return self.cached_balance

    def _is_valid(self):
        start_month = 1 if self.semester.semester == Semester.SPRING else 7
        end_month = 8 if self.semester.semester == Semester.SPRING else 1
        end_year_offset = 0 if self.semester.semester == Semester.SPRING else 1
        end_day = calendar.monthrange(self.semester.year, end_month)[1]

        start = datetime.date(self.semester.year, start_month, 1)
        end = datetime.date(self.semester.year + end_year_offset, end_month, end_day)

        now = datetime.date.today()
        return start <= now and now <= end

    is_valid = property(_is_valid)

    def __str__(self):
        return str(self.user) + " (" + str(self.semester) + ")"


class WorkLog(models.Model):
    DEFAULT_VOUCHERS_PER_HOUR = 0.5
    LOCKED_FOR_EDITING_AFTER_DAYS = 10

    wallet = models.ForeignKey(Wallet, related_name='worklogs')
    date_issued = models.DateTimeField(auto_now_add=True)
    date_worked = models.DateField()
    work_group = models.CharField(max_length=20)
    hours = models.DecimalField(max_digits=8, decimal_places=2)
    vouchers = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    issuing_user = models.ForeignKey(User)
    comment = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-date_issued']

    def __str__(self):
        return '%s %s %s hours' % (self.wallet, self.date_worked, self.hours)

    def clean(self):
        if self.hours <= 0:
            raise ValidationError({'hours': _("Hours must be positive")})

        if self.vouchers is None:
            self.vouchers = self.calculate_vouchers(self.hours)
        elif self.vouchers <= 0:
            raise ValidationError({'vouchers': _("Vouchers must be positive")})

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(WorkLog, self).save(*args, **kwargs)
            self.wallet.calculate_balance()

    def calculate_vouchers(self, hours):
        return round(float(hours) * self.DEFAULT_VOUCHERS_PER_HOUR, 2)


class UseLog(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='uselogs')
    date_spent = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    vouchers = models.IntegerField()

    class Meta:
        ordering = ['-date_spent']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.calculate_balance()

    def clean(self):
        if self.vouchers is None or self.vouchers <= 0 or (self.vouchers % 1) != 0:
            raise ValidationError({'vouchers': _('Vouchers must be a positive whole number')})

    def __str__(self):
        comment = ' (%s)' % self.comment if self.comment else ''
        return "%s - %s at %s%s" % (self.wallet, self.vouchers, self.date_spent.strftime('%Y-%m-%d %H:%M'), comment)
