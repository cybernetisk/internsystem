from rest_framework import serializers

from core.serializers import UserSerializer, CardSerializer, SemesterSerializer
from intern.models import AccessLevel, Intern, InternCard, InternGroup, InternRole,  Role


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = (
            'id', 'name', 'uio_name', 'description'
        )


class InternGroupSerializer(serializers.ModelSerializer):
    leader = UserSerializer()

    class Meta:
        model = InternGroup
        fields = (
            'id', 'name', 'leader', 'description'
        )


class RoleSerializer(serializers.ModelSerializer):
    groups = InternGroupSerializer(many=True)
    access_levels = AccessLevelSerializer(many=True)

    class Meta:
        model = Role
        fields = (
            'id', 'name', 'description', 'groups', 'access_levels'
        )


class InternRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = InternRole
        fields = (
            'id', 'role', 'date_added'
        )


class InternSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    roles = InternRoleSerializer(many=True, allow_null=True)

    class Meta:
        model = Intern
        fields = (
            'id', 'user', 'active', 'comments',
            'roles', 'registered', 'left'
        )


class SimpleInternSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Intern
        fields = (
            'id', 'user', 'comments'
        )


class InternRoleFullSerializer(InternRoleSerializer):
    role = RoleSerializer()
    intern = SimpleInternSerializer()
    semesters = SemesterSerializer(many=True)

    class Meta:
        model = InternRole
        fields = (
            'id', 'intern', 'role', 'semesters', 'date_access_given', 'date_access_revoked',
            'date_added', 'date_removed'
        )


class AddInternRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=15)

    class Meta:
        model = InternRole
        fields = (
            'username', 'role'
        )

class InternCardSerializer(serializers.ModelSerializer):
    intern = InternSerializer()
    internroles = InternRoleSerializer(many=True)
    semester = SemesterSerializer()

    class Meta:
        model = InternCard
        fields = ('intern', 'internroles', 'semester', 'date_made', 'made_by')

class AddInternCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternCard
        fields = ('intern', 'internroles')
