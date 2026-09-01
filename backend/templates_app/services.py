from datetime import datetime
from bson import ObjectId
from database.repositories import TemplateRepository, TriggerRepository

class TemplateService:
    @staticmethod
    def get_templates_for_trigger(trigger_id):
        if isinstance(trigger_id, str):
            trigger_id = ObjectId(trigger_id)
        return TemplateRepository.find({"trigger_id": trigger_id})

    @staticmethod
    def get_template(template_id):
        return TemplateRepository.find_by_id(template_id)

    @staticmethod
    def save_template(data):
        trigger_id = ObjectId(data['trigger_id'])
        if not TriggerRepository.find_by_id(trigger_id):
            raise ValueError(f"Trigger {trigger_id} does not exist")
            
        existing = TemplateRepository.find_by_trigger_and_channel(trigger_id, data['channel'])
        
        template_data = {
            **data,
            "trigger_id": trigger_id,
            "updated_at": datetime.utcnow()
        }
        
        if existing:
            TemplateRepository.update_one({"_id": existing["_id"]}, template_data)
            return TemplateRepository.find_by_id(existing["_id"])
        else:
            template_data["created_at"] = datetime.utcnow()
            return TemplateRepository.insert_one(template_data)

    @staticmethod
    def delete_template(template_id):
        return TemplateRepository.delete_one({"_id": template_id})
