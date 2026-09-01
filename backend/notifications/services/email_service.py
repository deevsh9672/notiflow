from django.core.mail import send_mail
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(to, subject, body):
        if settings.NOTIFICATION_MOCK_MODE:
            print(f"[MOCK EMAIL] To: {to} | Subject: {subject} | Body: {body}")
            return {"status": "mocked", "id": "mock_email_123"}
            
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise ValueError("SMTP credentials are not configured in environment variables.")
            
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to],
                fail_silently=False,
            )
            return {"status": "sent", "provider": "smtp"}
        except Exception as e:
            raise ValueError(f"SMTP Error: {str(e)}")
