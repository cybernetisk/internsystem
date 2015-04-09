from rest_framework import serializers

from cal.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        depth = 0
