from django.db import models
from django.utils import timezone

from core.models import User, Semester, Card
from core.utils import get_semester
from members.models import Member

# Create your models here.
class AccessLevel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    uio_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class InternGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(User)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    groups = models.ManyToManyField(InternGroup, related_name='roles')
    access_levels = models.ManyToManyField(AccessLevel)

    def __str__(self):
        return self.name



class Intern(models.Model):
    user = models.OneToOneField(User, unique=True)
    active = models.BooleanField(default=True)
    comments = models.CharField(max_length=300, null=True, blank=True)
    registered = models.DateField(auto_now_add=True)
    left = models.DateField(null=True)

    def __str__(self):
        return str(self.user)

    def update_left(self):
        left = True
        for role in self.roles:
            if role.date_removed is None:
                left = False
        if left:
            self.left = timezone.now()


class InternRole(models.Model):
    intern = models.ForeignKey(Intern, related_name='roles')
    role = models.ForeignKey(Role, related_name='intern')
    semesters = models.ManyToManyField(Semester, related_name='internroles')
    comments = models.CharField(max_length=300, null=True, blank=True)

    date_added = models.DateField(auto_now_add=True)
    date_removed = models.DateField(null=True, blank=True)

    date_access_given = models.DateField(null=True, blank=True)
    date_access_revoked = models.DateField(null=True, blank=True)

    recieved_interncard = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.role, self.intern)

    class Meta:
        unique_together = ("intern", "role")

class InternCard(models.Model):
    intern = models.ForeignKey(Intern)
    internrole = models.ManyToManyField(InternRole)
    semester = models.ForeignKey(Semester)

    date_made = models.DateField(null=True)
    made_by = models.ForeignKey(User)

    class Meta:
        unique_together = ('intern', 'semester')
