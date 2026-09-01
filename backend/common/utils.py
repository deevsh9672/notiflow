from bson import ObjectId
from datetime import datetime

def serialize_mongo_document(doc):
    """
    Recursively converts MongoDB ObjectId to strings and datetime to ISO format strings.
    """
    if doc is None:
        return None
        
    if isinstance(doc, list):
        return [serialize_mongo_document(item) for item in doc]
        
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            # Standardize _id to id in responses (optional, but common)
            # We'll keep _id as well or just convert it to string
            if key == "_id":
                serialized["_id"] = str(value) if value else None
                serialized["id"] = str(value) if value else None
            else:
                serialized[key] = serialize_mongo_document(value)
        return serialized
        
    if isinstance(doc, ObjectId):
        return str(doc)
        
    if isinstance(doc, datetime):
        return doc.isoformat()
        
    return doc
