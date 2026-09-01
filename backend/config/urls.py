from django.urls import path, include
from database.mongodb import create_indexes

# Create MongoDB indexes on startup
try:
    create_indexes()
except Exception as e:
    print(f"Warning: Could not create MongoDB indexes on startup: {e}")

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/triggers/', include('triggers.urls')),
    path('api/templates/', include('templates_app.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/logs/', include('notification_logs.urls')),
]
