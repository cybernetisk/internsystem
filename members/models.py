from core.models import *


# Create your models here.
class Member(models.Model):
    semester = models.ForeignKey(Semester)
    lifetime = models.BooleanField(blank=False, help_text='Lifetime member')
    honorary = models.BooleanField(blank=False, help_text='Honorary member')
    date_joined = models.DateTimeField()
    user = models.ForeignKey(User, null=True)
    seller = models.ForeignKey(User)


class InternGroup(models.Model):
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(User)
    description = models.CharField(max_length=300)


class InternRole(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    role_groups = models.ManyToManyField(InternGroup, related_name='groups')


class InternMember(models.Model):
    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    recivedCard = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    comments = models.CharField(max_length=300)
    roles = models.ManyToManyField(InternRole, related_name='roles')