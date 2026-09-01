import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR.parent / '.env')

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'corsheaders',
    # Our apps
    'accounts',
    'triggers',
    'notifications',
    'templates_app',
    'notification_logs',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Since we are not using Django's auth/sessions, we remove those middlewares.
]

CORS_ALLOW_ALL_ORIGINS = True  # For dev/sandbox. Change to CORS_ALLOWED_ORIGINS in prod


ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# Using MongoDB only via PyMongo, so we disable Django's relational DB configuration.
DATABASES = {}

# MongoDB Configuration
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'notifyflow')

# JWT Authentication
JWT_SECRET = os.environ.get('JWT_SECRET', SECRET_KEY)

# External APIs
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID', '')
POSTMARKAPP_TOKEN = os.environ.get('POSTMARKAPP_TOKEN', '')
POSTMARK_FROM_EMAIL = os.environ.get('POSTMARK_FROM_EMAIL', '')
ONESIGNAL_APP_ID = os.environ.get('ONESIGNAL_APP_ID', '')
ONESIGNAL_REST_API_KEY = os.environ.get('ONESIGNAL_REST_API_KEY', '')

NOTIFICATION_MOCK_MODE = os.environ.get('NOTIFICATION_MOCK_MODE', 'True') == 'True'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'common.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'EXCEPTION_HANDLER': 'common.exceptions.custom_exception_handler',
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
