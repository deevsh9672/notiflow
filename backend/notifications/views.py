from datetime import datetime
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.permissions import IsAdminUser, IsAuthenticated
from database.repositories import TriggerRepository, UserRepository, PushSubscriptionRepository
from .serializers import TriggerEventSerializer, PushSubscriptionSerializer
from .services.notification_service import NotificationService
from common.utils import serialize_mongo_document

class TriggerEventView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TriggerEventSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            trigger = TriggerRepository.find_by_slug(data['trigger_slug'])
            if not trigger:
                return Response({"error": "Trigger not found"}, status=status.HTTP_404_NOT_FOUND)
                
            user = UserRepository.find_by_id(data['user_id'])
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                
            # Run asynchronously in real app; synchronous here for simplicity
            NotificationService.trigger_event(user, trigger, data.get('variables', {}))
            
            return Response({"message": "Event triggered successfully"})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WebPushSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PushSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            sub_data = {
                "user_id": ObjectId(request.user.id),
                "subscription_id": data['subscription_id'],
                "endpoint": data['endpoint'],
                "provider": data['provider'],
                "is_active": True,
                "created_at": datetime.utcnow()
            }
            
            # Deactivate any existing with same sub ID just in case
            PushSubscriptionRepository.update_one(
                {"subscription_id": data['subscription_id']},
                {"is_active": False}
            )
            
            sub = PushSubscriptionRepository.insert_one(sub_data)
            return Response(serialize_mongo_document(sub), status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
