from django.db import models

from core.models import User, Semester, Card
from members.models import Member


# Create your models here.
class AccessLevel(models.Model):
    name = models.CharField(max_length=20)
    uio_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class InternGroup(models.Model):
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(User)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class InternRole(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    groups = models.ManyToManyField(InternGroup, related_name='groups')
    access_levels = models.ManyToManyField(AccessLevel)

    def __str__(self):
        return self.name



class Intern(models.Model):
    user = models.ForeignKey(User)
    member = models.ForeignKey(Member)
    semester = models.ForeignKey(Semester)
    recived_card = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    comments = models.CharField(max_length=300, null=True, blank=True)
    roles = models.ManyToManyField(InternRole, related_name='roles')

    def __str__(self):
        return "%s %s" % (self.user, self.semester)

    def cards(self):
        cards = self.user.card_set.all()
        return cards

    class Meta:
        unique_together = ("user", "semester")
