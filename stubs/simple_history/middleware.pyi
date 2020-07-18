from typing import Any

from django.utils.deprecation import MiddlewareMixin

from .models import HistoricalRecords as HistoricalRecords

class HistoryRequestMiddleware(MiddlewareMixin):
    def process_request(self, request: Any) -> None: ...
    def process_response(self, request: Any, response: Any): ...
