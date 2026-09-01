from rest_framework import serializers

class TriggerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    event_type = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
