import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from database.repositories import UserRepository
from bson import ObjectId

class MongoDBUser:
    """Mock user object to satisfy DRF's request.user expectations."""
    def __init__(self, user_data):
        self.user_data = user_data
        self.is_authenticated = True
        self.id = str(user_data.get('_id'))
        
    @property
    def role(self):
        return self.user_data.get('role', 'USER')
        
    @property
    def email(self):
        return self.user_data.get('email')


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
            
        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            return None
            
        if len(parts) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')
            
        token = parts[1]
        
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
            
        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('Token contains no user_id')
            
        try:
            user = UserRepository.find_by_id(ObjectId(user_id))
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid user_id format')
            
        if not user:
            raise exceptions.AuthenticationFailed('User not found')
            
        return (MongoDBUser(user), token)
