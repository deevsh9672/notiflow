import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from database.repositories import UserRepository

class AccountService:
    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_jwt(user):
        payload = {
            'user_id': str(user['_id']),
            'email': user['email'],
            'role': user.get('role', 'USER'),
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    @classmethod
    def register_user(cls, name, email, phone, password, role="USER"):
        if UserRepository.find_by_email(email):
            raise ValueError("User with this email already exists")

        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": cls.hash_password(password),
            "role": role,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        user = UserRepository.insert_one(user_data)
        
        # Omit password in return
        user.pop('password', None)
        return user

    @classmethod
    def login(cls, email, password):
        user = UserRepository.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
            
        if not cls.check_password(password, user['password']):
            raise ValueError("Invalid email or password")
            
        UserRepository.update_one({"_id": user["_id"]}, {"last_login": datetime.utcnow()})
        token = cls.generate_jwt(user)
        
        user.pop('password', None)
        return user, token
