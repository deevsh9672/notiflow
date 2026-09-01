from datetime import datetime
from database.repositories import TriggerRepository

class TriggerService:
    @staticmethod
    def get_all_triggers():
        return TriggerRepository.find()

    @staticmethod
    def get_trigger(trigger_id):
        return TriggerRepository.find_by_id(trigger_id)

    @staticmethod
    def get_trigger_by_slug(slug):
        return TriggerRepository.find_by_slug(slug)

    @staticmethod
    def create_trigger(data):
        if TriggerRepository.find_by_slug(data['slug']):
            raise ValueError(f"Trigger with slug {data['slug']} already exists")
            
        trigger_data = {
            **data,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return TriggerRepository.insert_one(trigger_data)

    @staticmethod
    def update_trigger(trigger_id, data):
        data["updated_at"] = datetime.utcnow()
        success = TriggerRepository.update_one({"_id": trigger_id}, data)
        if not success:
            raise ValueError("Trigger not found or update failed")
        return TriggerRepository.find_by_id(trigger_id)

    @staticmethod
    def delete_trigger(trigger_id):
        return TriggerRepository.delete_one({"_id": trigger_id})
