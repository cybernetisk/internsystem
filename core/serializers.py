from rest_framework import serializers
from core.models import User, Semester, Card


class UserSimpleGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname')


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email')


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
                  'groups', 'user_permissions')


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('year', 'semester')

class CardSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()
    class Meta:
        model = Card
        fields = ('user', 'card_number', 'disabled', 'comment')
