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
    user = models.OneToOneField(User, unique=True, related_name='intern')
    comments = models.CharField(max_length=300, null=True, blank=True)
    registered = models.DateField(auto_now_add=True)
    left = models.DateField(null=True)

    def __str__(self):
        return str(User.objects.prefetch_related().all()[0])

    def update_left(self):
        """
        Update the left field with date person stopped being intern or remove the date if person rejoins.
        :return: Nothing.
        """
        left = True
        for role in InternRole.objects.select_related().all():
            if role.date_removed is None:
                left = False
        if left:
            self.left = timezone.now()
        else:
            self.left = None
        self.save()

    def _active(self):
        for role in InternRole.objects.select_related().all():
            if role.date_removed is None:
                return True
        return False
    active = property(_active)



class InternRole(models.Model):
    intern = models.ForeignKey(Intern, related_name='roles')
    role = models.ForeignKey(Role, related_name='intern')
    semesters = models.ManyToManyField(Semester, related_name='internroles')
    comments = models.CharField(max_length=300, null=True, blank=True)

    created_by = models.ForeignKey(User, related_name='internroles_created')
    last_editor = models.ForeignKey(User, related_name='internroles_edited')
    removed_by = models.ForeignKey(User, related_name='internroles_removed', null=True, blank=True)

    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now_add=True)
    date_removed = models.DateField(null=True, blank=True)

    access_given = models.BooleanField(default=False)
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
