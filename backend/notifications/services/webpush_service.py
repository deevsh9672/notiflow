import requests
from django.conf import settings

class WebPushService:
    @staticmethod
    def send_push(subscription_id, title, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK WEBPUSH] SubID: {subscription_id} | Title: {title} | Body: {body}")
            return {"status": "mocked", "id": "mock_push_123"}
            
        app_id = settings.ONESIGNAL_APP_ID
        api_key = settings.ONESIGNAL_REST_API_KEY
        
        if not app_id or not api_key:
            raise ValueError("OneSignal configuration is missing")
            
        url = "https://onesignal.com/api/v1/notifications"
        headers = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "app_id": app_id,
            "include_player_ids": [subscription_id],
            "headings": {"en": title},
            "contents": {"en": body}
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
