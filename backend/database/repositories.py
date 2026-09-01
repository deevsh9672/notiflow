from bson import ObjectId
from database.mongodb import (
    users_collection,
    triggers_collection,
    notification_templates_collection,
    notification_logs_collection,
    push_subscriptions_collection,
    variable_mappings_collection
)

class BaseRepository:
    collection = None

    @classmethod
    def find(cls, query=None, sort=None, limit=None, skip=None):
        query = query or {}
        cursor = cls.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)

    @classmethod
    def find_one(cls, query):
        if "_id" in query and isinstance(query["_id"], str):
            try:
                query["_id"] = ObjectId(query["_id"])
            except:
                pass
        return cls.collection.find_one(query)

    @classmethod
    def find_by_id(cls, document_id):
        if isinstance(document_id, str):
            try:
                document_id = ObjectId(document_id)
            except:
                return None
        return cls.collection.find_one({"_id": document_id})

    @classmethod
    def insert_one(cls, document):
        result = cls.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    @classmethod
    def update_one(cls, query, update_data, upsert=False):
        if "_id" in query and isinstance(query["_id"], str):
            try:
                query["_id"] = ObjectId(query["_id"])
            except:
                pass
        
        # If update_data doesn't have MongoDB operators, assume $set
        if not any(k.startswith("$") for k in update_data.keys()):
            update_data = {"$set": update_data}
            
        result = cls.collection.update_one(query, update_data, upsert=upsert)
        return result.modified_count > 0 or result.upserted_id is not None

    @classmethod
    def delete_one(cls, query):
        if "_id" in query and isinstance(query["_id"], str):
            try:
                query["_id"] = ObjectId(query["_id"])
            except:
                pass
        result = cls.collection.delete_one(query)
        return result.deleted_count > 0

    @classmethod
    def count(cls, query=None):
        query = query or {}
        return cls.collection.count_documents(query)
        
    @classmethod
    def paginate(cls, query=None, page=1, page_size=10, sort=None):
        query = query or {}
        skip = (page - 1) * page_size
        items = cls.find(query=query, sort=sort, limit=page_size, skip=skip)
        total = cls.count(query)
        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }


class UserRepository(BaseRepository):
    collection = users_collection
    
    @classmethod
    def find_by_email(cls, email):
        return cls.find_one({"email": email})


class TriggerRepository(BaseRepository):
    collection = triggers_collection
    
    @classmethod
    def find_by_slug(cls, slug):
        return cls.find_one({"slug": slug})


class TemplateRepository(BaseRepository):
    collection = notification_templates_collection
    
    @classmethod
    def find_by_trigger_and_channel(cls, trigger_id, channel):
        if isinstance(trigger_id, str):
            trigger_id = ObjectId(trigger_id)
        return cls.find_one({"trigger_id": trigger_id, "channel": channel})


class NotificationLogRepository(BaseRepository):
    collection = notification_logs_collection


class PushSubscriptionRepository(BaseRepository):
    collection = push_subscriptions_collection
    
    @classmethod
    def find_by_user(cls, user_id):
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)
        return cls.find({"user_id": user_id, "is_active": True})


class VariableMappingRepository(BaseRepository):
    collection = variable_mappings_collection
