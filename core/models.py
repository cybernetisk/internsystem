from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Semester(models.Model):
    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(Semester, self).save(*args, **kwargs)

    date_start = models.DateTimeField(blank=True)
    date_end = models.DateTimeField(blank=True)

class CybUser(models.Model):
    def save(self, *args, **kwargs):
        with transaction.atomic():
            super(CybUser, self).save(*args, **kwargs)

    user = models.OneToOneField(User)
