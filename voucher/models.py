from django.db import models, transaction
from django.db.models import Sum
from core.models import User, Semester, NfcCard
from decimal import Decimal

import calendar
import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    cached_balance = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, editable=False
    )
    cached_vouchers = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, editable=False
    )
    cached_vouchers_used = models.IntegerField(default=0, editable=False)

    class Meta:
        abstract = True

    def _calculate_balance(self, vouchers_earned, vouchers_used):
        self.cached_balance = vouchers_earned - vouchers_used
        self.cached_vouchers = vouchers_earned
        self.cached_vouchers_used = vouchers_used
        self.save()
        return self.cached_balance

    def _is_valid(self):
        start_month = 1 if self.semester.semester == Semester.SPRING else 7
        end_month = 8 if self.semester.semester == Semester.SPRING else 1

        # Corona-exception in 2020.
        if self.semester.semester == Semester.SPRING and self.semester.year == 2020:
            end_month = 9

        # Corona-exception in 2021
        if self.semester.semester == Semester.FALL and self.semester.year == 2020:
            end_month = 7

        end_year_offset = 0 if self.semester.semester == Semester.SPRING else 1
        end_day = calendar.monthrange(self.semester.year, end_month)[1]

        start = datetime.date(self.semester.year, start_month, 1)
        end = datetime.date(self.semester.year + end_year_offset, end_month, end_day)

        now = datetime.date.today()
        return start <= now and now <= end

    is_valid = property(_is_valid)


class VoucherWallet(Wallet):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cached_hours = models.DecimalField(
        default=0, max_digits=8, decimal_places=2, editable=False
    )

    class Meta:
        unique_together = ("user", "semester")
        ordering = ["user__username"]

    def calculate_balance(self):
        vouchers_earned = WorkLog.objects.filter(wallet=self).aggregate(
            sum=Sum("vouchers")
        )["sum"] or Decimal(0)
        vouchers_used = VoucherUseLog.objects.filter(wallet=self).aggregate(
            sum=Sum("vouchers")
        )["sum"] or Decimal(0)
        hours = WorkLog.objects.filter(wallet=self).aggregate(sum=Sum("hours"))[
            "sum"
        ] or Decimal(0)
        self.cached_hours = hours
        return super()._calculate_balance(vouchers_earned, vouchers_used)

    def __str__(self):
        return str(self.user) + " (" + str(self.semester) + ")"


class CoffeeWallet(Wallet):
    card = models.ForeignKey(NfcCard, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("card", "semester")
        ordering = ["card__card_uid"]

    def calculate_balance(self):
        vouchers_earned = CoffeeRegisterLog.objects.filter(wallet=self).aggregate(
            sum=Sum("vouchers")
        )["sum"] or Decimal(0)
        vouchers_used = CoffeeUseLog.objects.filter(wallet=self).aggregate(
            sum=Sum("vouchers")
        )["sum"] or Decimal(0)

        return super()._calculate_balance(vouchers_earned, vouchers_used)

    def __str__(self):
        return str(self.card) + " (" + str(self.semester) + ")"


class RegisterLog(models.Model):
    LOCKED_FOR_EDITING_AFTER_DAYS = 2

    date_issued = models.DateTimeField(auto_now_add=True)
    issuing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-date_issued"]

    def clean(self):
        if self.vouchers <= 0:
            raise ValidationError({"vouchers": _("Vouchers must be positive")})

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.calculate_balance()

    def is_locked(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - self.date_issued).days > self.LOCKED_FOR_EDITING_AFTER_DAYS


class CoffeeRegisterLog(RegisterLog):
    wallet = models.ForeignKey(
        CoffeeWallet, related_name="registerlogs", on_delete=models.CASCADE
    )
    vouchers = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%s %s vouchers" % (self.wallet, self.vouchers)


class WorkLog(RegisterLog):
    DEFAULT_VOUCHERS_PER_HOUR = 0.5

    wallet = models.ForeignKey(
        VoucherWallet, related_name="worklogs", on_delete=models.CASCADE
    )
    date_worked = models.DateField()
    work_group = models.CharField(max_length=20)
    hours = models.DecimalField(max_digits=8, decimal_places=2)
    vouchers = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return "%s %s %s hours" % (self.wallet, self.date_worked, self.hours)

    def clean(self):
        if self.vouchers is None:
            self.vouchers = self.calculate_vouchers(self.hours)
        elif self.hours <= 0:
            raise ValidationError({"hours": _("Hours must be positive")})

    def calculate_vouchers(self, hours):
        return round(float(hours) * self.DEFAULT_VOUCHERS_PER_HOUR, 2)


class UseLog(models.Model):
    date_spent = models.DateTimeField(auto_now_add=True)
    issuing_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, null=True, blank=True)
    vouchers = models.IntegerField()

    class Meta:
        abstract = True
        ordering = ["-date_spent"]

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.wallet.calculate_balance()

    def clean(self):
        if self.vouchers is None or self.vouchers <= 0 or (self.vouchers % 1) != 0:
            raise ValidationError(
                {"vouchers": _("Vouchers must be a positive whole number")}
            )

    def __str__(self):
        comment = " (%s)" % self.comment if self.comment else ""
        return "%s - %s at %s%s" % (
            self.wallet,
            self.vouchers,
            self.date_spent.strftime("%Y-%m-%d %H:%M"),
            comment,
        )


class VoucherUseLog(UseLog):
    wallet = models.ForeignKey(
        VoucherWallet, related_name="uselogs", on_delete=models.CASCADE
    )


class CoffeeUseLog(UseLog):
    wallet = models.ForeignKey(
        CoffeeWallet, related_name="uselogs", on_delete=models.CASCADE
    )
