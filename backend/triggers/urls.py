from django.urls import path
from .views import TriggerListView, TriggerDetailView

urlpatterns = [
    path('', TriggerListView.as_view(), name='trigger-list'),
    path('<str:pk>/', TriggerDetailView.as_view(), name='trigger-detail'),
]
