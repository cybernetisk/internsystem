from rest_framework import serializers

from members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('id', 'name', 'email', 'semester', 'lifetime', 'honorary')


class AddMemberSerializer(serializers.Serializer):
    '''
    class Meta:
        model = Member
        field = ('id', 'name', 'email', 'lifetime', 'honorary', 'user')
    '''
    name = serializers.CharField(max_length=50, help_text='name of user, max 50 letters')
    email = serializers.EmailField(allow_blank=True)
    lifetime = serializers.BooleanField(help_text='Is the member a lifetime member?')