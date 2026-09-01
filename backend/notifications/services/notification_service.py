import re
from datetime import datetime
from bson import ObjectId
from database.repositories import (
    TemplateRepository, 
    NotificationLogRepository,
    PushSubscriptionRepository
)
from .whatsapp_service import WhatsAppService
from .email_service import EmailService
from .webpush_service import WebPushService

class NotificationService:
    @staticmethod
    def replace_variables(text, variables_data):
        if not text:
            return text
        
        def replacer(match):
            var_name = match.group(1)
            return str(variables_data.get(var_name, match.group(0)))
            
        return re.sub(r'\{\{([^}]+)\}\}', replacer, text)

    @classmethod
    def trigger_event(cls, user, trigger, variables_data=None):
        variables_data = variables_data or {}
        # Auto-inject user data
        variables_data.update({
            "user_name": user.get('name', ''),
            "email": user.get('email', ''),
            "phone": user.get('phone', '')
        })

        templates = TemplateRepository.find({
            "trigger_id": trigger["_id"],
            "is_enabled": True
        })

        for template in templates:
            cls.dispatch_notification(user, trigger, template, variables_data)

    @classmethod
    def dispatch_notification(cls, user, trigger, template, variables_data):
        channel = template['channel']
        subject = cls.replace_variables(template.get('subject', ''), variables_data)
        title = cls.replace_variables(template.get('title', ''), variables_data)
        body = cls.replace_variables(template.get('body', ''), variables_data)
        
        log_data = {
            "user_id": user["_id"],
            "trigger_id": trigger["_id"],
            "template_id": template["_id"],
            "channel": channel,
            "subject": subject or title,
            "message": body,
            "status": "PENDING",
            "provider_response": {},
            "error_message": None,
            "created_at": datetime.utcnow()
        }

        recipient = None
        try:
            if channel == 'WHATSAPP':
                recipient = user.get('phone')
                if not recipient:
                    raise ValueError("User has no phone number")
                log_data["recipient"] = recipient
                response = WhatsAppService.send_message(recipient, body)
                
            elif channel == 'EMAIL':
                recipient = variables_data.get('override_email') or user.get('email')
                if not recipient:
                    raise ValueError("User has no email")
                log_data["recipient"] = recipient
                response = EmailService.send_email(recipient, subject, body)
                
            elif channel == 'WEB_PUSH':
                subs = PushSubscriptionRepository.find_by_user(user["_id"])
                if not subs:
                    raise ValueError("No active web push subscriptions")
                # Send to first active sub for simplicity, or iterate
                recipient = subs[0]["subscription_id"]
                log_data["recipient"] = recipient
                response = WebPushService.send_push(recipient, title, body)
            else:
                raise ValueError(f"Unknown channel {channel}")

            log_data["status"] = "SENT"
            log_data["provider_response"] = response

        except Exception as e:
            log_data["status"] = "FAILED"
            log_data["error_message"] = str(e)
        finally:
            NotificationLogRepository.insert_one(log_data)
