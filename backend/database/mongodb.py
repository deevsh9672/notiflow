import os
from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        mongodb_uri = getattr(settings, 'MONGODB_URI', os.environ.get('MONGODB_URI'))
        db_name = getattr(settings, 'MONGODB_DATABASE', os.environ.get('MONGODB_DATABASE', 'notifyflow'))
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI is not set in settings or environment variables")
            
        self._client = MongoClient(mongodb_uri)
        self._db = self._client[db_name]

    @property
    def db(self):
        return self._db

    def get_collection(self, collection_name):
        return self._db[collection_name]

# Global instance
mongo_client = MongoDBClient()

# Collections
users_collection = mongo_client.get_collection('users')
triggers_collection = mongo_client.get_collection('triggers')
notification_templates_collection = mongo_client.get_collection('notification_templates')
notification_logs_collection = mongo_client.get_collection('notification_logs')
push_subscriptions_collection = mongo_client.get_collection('push_subscriptions')
variable_mappings_collection = mongo_client.get_collection('variable_mappings')

def create_indexes():
    """Create required indexes for collections."""
    from pymongo import ASCENDING
    
    # users: email unique
    users_collection.create_index([("email", ASCENDING)], unique=True)
    
    # triggers: slug unique
    triggers_collection.create_index([("slug", ASCENDING)], unique=True)
    
    # notification_templates: trigger_id + channel unique
    notification_templates_collection.create_index(
        [("trigger_id", ASCENDING), ("channel", ASCENDING)], 
        unique=True
    )
    
    # notification_logs: user_id, trigger_id, created_at
    notification_logs_collection.create_index([("user_id", ASCENDING)])
    notification_logs_collection.create_index([("trigger_id", ASCENDING)])
    notification_logs_collection.create_index([("created_at", ASCENDING)])
