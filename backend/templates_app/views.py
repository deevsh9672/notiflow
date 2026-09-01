from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.permissions import IsAdminUser
from .serializers import TemplateSerializer
from .services import TemplateService
from common.utils import serialize_mongo_document

class TemplateListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        trigger_id = request.query_params.get('trigger_id')
        if not trigger_id:
            return Response({"error": "trigger_id query param is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        templates = TemplateService.get_templates_for_trigger(trigger_id)
        return Response(serialize_mongo_document(templates))

    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                template = TemplateService.save_template(serializer.validated_data)
                return Response(serialize_mongo_document(template), status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TemplateDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        template = TemplateService.get_template(pk)
        if not template:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_mongo_document(template))

    def delete(self, request, pk):
        success = TemplateService.delete_template(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
