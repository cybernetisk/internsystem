from django.db import models, transaction
from datetime import datetime
from core.models import CybUser, Semester

# Create your models here.
class BongWallet(models.Model):
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

    wallet = models.ForeignKey(BongWallet)

    action = models.CharField(max_length=1, choices=BONG_ACTION_CHOICES, default=ISSUED)
    date_issued = models.DateTimeField(default=datetime.now, blank=True)
    issuing_user = models.ForeignKey(CybUser, related_name='issuing_user')
    comment = models.TextField(default='')

    # bong details
    group = models.TextField(default='')
    hours = models.DecimalField(default=0, max_digits=2, decimal_places=2)
    bongs = models.DecimalField(default=0, max_digits=8, decimal_places=2)


    # Revoke stuff
    is_revoked = models.BooleanField(default=False)
    date_revoked = models.DateTimeField(default=False, blank=True)
    revoking_user = models.ForeignKey(CybUser, related_name='revoking_user', blank=True, null=True)
