from database.repositories import NotificationLogRepository
from pymongo import DESCENDING

class NotificationLogService:
    @staticmethod
    def get_logs(page=1, page_size=20):
        # Sort by created_at DESC
        return NotificationLogRepository.paginate(
            query={},
            page=page,
            page_size=page_size,
            sort=[("created_at", DESCENDING)]
        )
