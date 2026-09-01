from rest_framework import serializers

class TriggerEventSerializer(serializers.Serializer):
    trigger_slug = serializers.CharField()
    user_id = serializers.CharField()
    variables = serializers.DictField(required=False, default=dict)

class PushSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.CharField()
    endpoint = serializers.CharField()
    provider = serializers.CharField(default="ONESIGNAL")
