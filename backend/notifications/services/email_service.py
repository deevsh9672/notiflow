import requests
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body}")
            return {"status": "mocked", "id": "mock_email_123"}
            
        token = settings.POSTMARKAPP_TOKEN
        from_email = settings.POSTMARK_FROM_EMAIL
        
        if not token or not from_email:
            raise ValueError("Postmark configuration is missing")
            
        url = "https://api.postmarkapp.com/email"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": token
        }
        payload = {
            "From": from_email,
            "To": to,
            "Subject": subject,
            "TextBody": body
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
