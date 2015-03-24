from django.db import models
from datetime import datetime

# Create your models here.
class Semester(models.Model):
    date_start = models.DateTimeField(blank=True)
    date_end = models.DateTimeField(blank=True)

class InternGroup(models.Model):
    pass

class CybUser(models.Model):
    pass
