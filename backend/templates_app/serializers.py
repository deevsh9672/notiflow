from rest_framework import serializers

class TemplateSerializer(serializers.Serializer):
    trigger_id = serializers.CharField()
    channel = serializers.ChoiceField(choices=["WHATSAPP", "EMAIL", "WEB_PUSH"])
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    subject = serializers.CharField(max_length=255, required=False, allow_blank=True)
    body = serializers.CharField()
    variables = serializers.ListField(child=serializers.CharField(), required=False)
    is_enabled = serializers.BooleanField(default=True)
