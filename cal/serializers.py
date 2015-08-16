from rest_framework import serializers

from core.serializers import UserSimpleSerializer
from cal.models import Event


class EventGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = ('id', 'start', 'end', 'is_allday', 'title', 'description', 'link',
                  'is_published', 'is_public', 'is_external', 'in_escape', 'is_cancelled')


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSimpleSerializer()

    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'start', 'end', 'is_allday', 'title', 'description', 'comment', 'link',
                  'is_published', 'is_public', 'is_external', 'in_escape', 'is_cancelled', 'organizer')


class EventWriteSerializer(EventSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = ('id', 'start', 'end', 'is_allday', 'title', 'description', 'comment', 'link',
                  'is_published', 'is_public', 'is_external', 'in_escape', 'is_cancelled', 'organizer')


class EscapeOccupiedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = ('start', 'end')
