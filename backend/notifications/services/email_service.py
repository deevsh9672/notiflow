import requests
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body}")
            return {"status": "mocked", "id": "mock_email_123"}
            
        api_key = settings.BREVO_API_KEY
        from_email = settings.BREVO_FROM_EMAIL
        
        if not api_key or not from_email:
            raise ValueError("Brevo configuration is missing")
            
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "api-key": api_key
        }
        payload = {
            "sender": {
                "name": "Notification System",
                "email": from_email
            },
            "to": [
                {
                    "email": to
                }
            ],
            "subject": subject,
            "textContent": body
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
