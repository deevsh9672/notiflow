import requests
from django.conf import settings

class WhatsAppService:
    @staticmethod
    def send_message(to, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK WHATSAPP] To: {to} | Body: {body}")
            return {"status": "mocked", "id": "mock_wa_123"}
            
        token = settings.WHATSAPP_ACCESS_TOKEN
        phone_number_id = settings.PHONE_NUMBER_ID
        
        if not token or not phone_number_id:
            raise ValueError("WhatsApp configuration is missing")
            
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body}
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
