from rest_framework import serializers
from django.utils import timezone

from core.serializers import UserSimpleSerializer
from cal.models import Event


class EventMomentSerializer(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, obj):
        val = getattr(obj, self.source)

        if obj.is_allday:
            val = timezone.localtime(val, timezone.utc).date()
        else:
            val = timezone.localtime(val)

        return val

    def to_internal_value(self, data):
        pass


class EventGuestSerializer(serializers.ModelSerializer):
    start = EventMomentSerializer()
    end = EventMomentSerializer()

    class Meta:
        model = Event
        depth = 0
        fields = (
            "id",
            "start",
            "end",
            "is_allday",
            "title",
            "description",
            "link",
            "is_published",
            "is_public",
            "is_external",
            "in_escape",
            "is_cancelled",
        )


class EventSerializer(serializers.ModelSerializer):
    start = EventMomentSerializer()
    end = EventMomentSerializer()
    organizer = UserSimpleSerializer()

    class Meta:
        model = Event
        depth = 1
        fields = (
            "id",
            "start",
            "end",
            "is_allday",
            "title",
            "description",
            "comment",
            "link",
            "is_published",
            "is_public",
            "is_external",
            "in_escape",
            "is_cancelled",
            "organizer",
        )


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = (
            "id",
            "start",
            "end",
            "is_allday",
            "title",
            "description",
            "comment",
            "link",
            "is_published",
            "is_public",
            "is_external",
            "in_escape",
            "is_cancelled",
            "organizer",
        )


class EscapeOccupiedEventSerializer(serializers.ModelSerializer):
    start = EventMomentSerializer()
    end = EventMomentSerializer()

    class Meta:
        model = Event
        depth = 0
        fields = ("start", "end", "is_allday")
