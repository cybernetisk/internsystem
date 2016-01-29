from core.models import *


# Create your models here.
class Member(models.Model):
    """
    The member model.

    It contains:
        -an optional reference to the user if it already exists.
        -the semester the membership was sold in
            (and for ordinary members also the semester it's valid for)
        -if the member got a lifetime or honorary membership.
        -the date the membership was sold
        -who sold it
        -name of the member
        -email address that can be blank

    Can only be one member with the same name and email address per semester.
    """
    user = models.ForeignKey(User, null=True, blank=True, related_name='user')
    semester = models.ForeignKey(Semester)
    lifetime = models.BooleanField(blank=False, help_text='Lifetime member')
    honorary = models.BooleanField(blank=False, help_text='Honorary member')
    date_joined = models.DateTimeField()
    seller = models.ForeignKey(User, related_name='seller')
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "email", "semester")


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
    member = models.ForeignKey(Member)
    semester = models.ForeignKey(Semester)
    recivedCard = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    comments = models.CharField(max_length=300)
    roles = models.ManyToManyField(InternRole, related_name='roles')