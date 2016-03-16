from rest_framework import serializers

from core.serializers import UserSimpleSerializer
from intern.models import Intern, InternRole, InternGroup, AccessLevel


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = (
            'name', 'uio_name', 'description'
        )


class InternGroupSerializer(serializers.ModelSerializer):
    leader = UserSimpleSerializer()

    class Meta:
        model = InternGroup
        fields = (
            'name', 'leader', 'description'
        )


class InternRoleSerializer(serializers.ModelSerializer):
    groups = InternGroupSerializer(many=True)
    access_levels = AccessLevelSerializer(many=True)

    class Meta:
        model = InternRole
        fields = (
            'id', 'name', 'description', 'groups', 'access_levels'
        )


class InternSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    roles = InternRoleSerializer(many=True)

    class Meta:
        model = Intern
        fields = (
            'id', 'user', 'semester', 'recived_card', 'active', 'comments',
            'roles', 'cards'
        )
