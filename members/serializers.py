from rest_framework import serializers

from members.models import Member
from members.permissions import has_permission
from core.serializers import SemesterSerializer


class MemberSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField('_can_edit')
    semester = SemesterSerializer()

    def _can_edit(self, instance):
        return has_permission(self.context['request'], instance, 'change')

    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'date_joined', 'semester', 'lifetime', 'honorary', 'can_edit')


class AddMemberSerializer(serializers.Serializer):
    '''
    class Meta:
        model = Member
        field = ('id', 'name', 'email', 'lifetime', 'honorary', 'user')
    '''
    name = serializers.CharField(max_length=50, help_text='name of user, max 50 letters')
    email = serializers.EmailField(allow_blank=True)
    lifetime = serializers.BooleanField(help_text='Is the member a lifetime member?')