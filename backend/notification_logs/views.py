from rest_framework.views import APIView
from rest_framework.response import Response
from common.permissions import IsAdminUser
from .services import NotificationLogService
from common.utils import serialize_mongo_document

class NotificationLogListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        logs_paginated = NotificationLogService.get_logs(page=page, page_size=page_size)
        return Response(serialize_mongo_document(logs_paginated))
