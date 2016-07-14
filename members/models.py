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
        -the date the member got a lifetimemembership
        -who sold it
        -name of the member
        -email address that can be blank
        -uio username that can be blank.

    Can only be one member with the same name and email address per semester.
    """
    user = models.ForeignKey(User, null=True, blank=True)
    semester = models.ForeignKey(Semester)
    lifetime = models.BooleanField(default=False, help_text='Lifetime member')
    honorary = models.BooleanField(default=False, help_text='Honorary member')
    date_joined = models.DateTimeField(auto_now_add=True)
    date_lifetime = models.DateTimeField(null=True)
    seller = models.ForeignKey(User, related_name='seller')
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    uio_username = models.CharField(max_length=15, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    last_edited_by = models.ForeignKey(User, related_name='modifier', null=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "email", "semester")

