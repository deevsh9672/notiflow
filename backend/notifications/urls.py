from django.urls import path
from .views import TriggerEventView, WebPushSubscriptionView

urlpatterns = [
    path('trigger/', TriggerEventView.as_view(), name='trigger-event'),
    path('push/subscribe/', WebPushSubscriptionView.as_view(), name='push-subscribe'),
]
