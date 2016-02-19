from rest_framework import serializers

from members.models import Member
from core.serializers import SemesterSerializer


class MemberSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer(read_only=True)


    class Meta:
        model = Member
        fields = (
        'id', 'name', 'email', 'date_joined', 'semester', 'lifetime', 'honorary', 'date_lifetime', 'uio_username')


class AddMemberSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, help_text='name of user, max 50 letters')
    email = serializers.EmailField(allow_blank=True)
    lifetime = serializers.BooleanField(help_text='Is the member a lifetime member?')
    uio_username = serializers.CharField(max_length=15, allow_blank=True, help_text='Your Uio username. Is optional.')