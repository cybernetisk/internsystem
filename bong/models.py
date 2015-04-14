from django.db import models, transaction
from django.utils.timezone import utc
from datetime import datetime
from core.models import CybUser, Semester
from decimal import Decimal

# Create your models here.
class BongWallet(models.Model):
    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(BongWallet, self).save(*args, **kwargs)

    semester = models.ForeignKey(Semester)
    user = models.OneToOneField(CybUser)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    total_assigned = models.DecimalField(default=0, max_digits=8, decimal_places=2)


class BongLog(models.Model):
    ISSUED = 'i'
    SPENDT = 's'

    BONG_ACTION_CHOICES = (
        (ISSUED, 'issued'),
        (SPENDT, 'spendt')
    )

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(BongLog, self).save(*args, **kwargs)

            self.wallet.balance = Decimal(self.wallet.balance) + Decimal(self.bongs)
            self.wallet.total_assigned = Decimal(self.wallet.total_assigned) + Decimal(self.bongs)
            self.wallet.save()

    wallet = models.ForeignKey(BongWallet)

    action = models.CharField(max_length=1, choices=BONG_ACTION_CHOICES, default=ISSUED)
    date_issued = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc), blank=True)
    issuing_user = models.ForeignKey(CybUser, related_name='issuing_user')
    comment = models.TextField(default='')

    # bong details
    group = models.TextField(default='')
    hours = models.DecimalField(default=Decimal(0), max_digits=4, decimal_places=2)
    bongs = models.DecimalField(default=Decimal(0), max_digits=8, decimal_places=2)


    # Revoke stuff
    is_revoked = models.BooleanField(default=False)
    date_revoked = models.DateTimeField(default=None, null=True, blank=True)
    revoking_user = models.ForeignKey(CybUser, related_name='revoking_user', default=None, blank=True, null=True)
