from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import datetime
from core.models import Semester

# Create your models here.
class BongLog(models.Model):
    # BongWallet

    # action issued / spendt
    # date issued
    # user issuer, how do we handle automatic issue by taking shift?

    # hours worked
    # bongs derived from hours
    # group, internal group identifier stuff?

    # comment

    # Revoke stuff
    #
    # is_revoked
    # user_revoked revoking user
    # date_revoked

    pass

class BongWallet(models.Model):
    semester = models.ForeignKey(Semester)

    user = models.OneToOneField(User)
    balance = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    total_assigned = models.DecimalField(default=0, max_digits=8, decimal_places=2)
