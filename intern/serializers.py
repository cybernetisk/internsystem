from rest_framework import serializers

from core.serializers import UserSerializer, CardSerializer
from intern.models import Intern, InternRole, InternGroup, AccessLevel


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


class InternRoleSerializer(serializers.ModelSerializer):
    groups = InternGroupSerializer(many=True)
    access_levels = AccessLevelSerializer(many=True)

    class Meta:
        model = InternRole
        fields = (
            'id', 'name', 'description', 'groups', 'access_levels'
        )


class InternRoleSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternRole
        fields = (
            'id', 'name'
        )

class InternSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    roles = InternRoleSimpleSerializer(many=True)
    cards = CardSerializer(many=True)

    class Meta:
        model = Intern
        fields = (
            'id', 'user', 'semester', 'recived_card', 'active', 'comments',
            'roles', 'cards'
        )