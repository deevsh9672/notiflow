from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.permissions import IsAdminUser
from .serializers import TriggerSerializer
from .services import TriggerService
from common.utils import serialize_mongo_document
from bson import ObjectId

class TriggerListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        triggers = TriggerService.get_all_triggers()
        return Response(serialize_mongo_document(triggers))

    def post(self, request):
        serializer = TriggerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                trigger = TriggerService.create_trigger(serializer.validated_data)
                return Response(serialize_mongo_document(trigger), status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TriggerDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        trigger = TriggerService.get_trigger(pk)
        if not trigger:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_mongo_document(trigger))

    def put(self, request, pk):
        serializer = TriggerSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                trigger = TriggerService.update_trigger(pk, serializer.validated_data)
                return Response(serialize_mongo_document(trigger))
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        success = TriggerService.delete_trigger(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
