import requests
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body}")
            return {"status": "mocked", "id": "mock_email_123"}
            
        api_key = settings.MAILJET_API_KEY
        secret_key = settings.MAILJET_SECRET_KEY
        from_email = settings.MAILJET_FROM_EMAIL
        
        if not api_key or not secret_key or not from_email:
            raise ValueError("Mailjet configuration is missing")
            
        url = "https://api.mailjet.com/v3.1/send"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "Messages": [
                {
                    "From": {
                        "Email": from_email,
                        "Name": "Notification System"
                    },
                    "To": [
                        {
                            "Email": to
                        }
                    ],
                    "Subject": subject,
                    "TextPart": body
                }
            ]
        }
        
        response = requests.post(url, auth=(api_key, secret_key), headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
