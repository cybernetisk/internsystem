from rest_framework import serializers

from core.serializers import UserSerializer, CardSerializer
from intern.models import Intern, Role, InternGroup, AccessLevel, InternRole


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
            'id', 'role', 'semester_start', 'semester_end'
        )


class InternSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cards = CardSerializer(many=True)
    roles = InternRoleSerializer(many=True, allow_null=True)

    class Meta:
        model = Intern
        fields = (
            'id', 'user', 'recived_card', 'active', 'comments',
            'cards', 'roles'
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

    class Meta:
        model = InternRole
        fields = (
            'id', 'intern', 'role', 'semester_start', 'semester_end'
        )

