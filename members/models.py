from core.models import *

# Create your models here.
class Member:
    semester = models.ForeignObject(Semester)
    lifetime = models.BooleanField(blank=False)
    honorary = models.BooleanField(blank=False)
    date_joined = models.DateTimeField()
    user = models.ForeignKey(User, null=True)
    seller = models.ForeignKey(User)


class intern_member:
    user = models.ForeignKey(User)
    semester = models.ForeignKey(Semester)
    recivedCard = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    comments = models.CharField(max_length=300)
    roles = models.ManyToManyRel(intern_role)


class intern_role:
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    groups = models.ManyToManyRel(intern_group)


class intern_group:
    name = models.CharField(max_length=50)
    leader = models.ForeignKey(User)
    description = models.CharField(max_length=300)