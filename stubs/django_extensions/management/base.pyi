from typing import Any

from django.core.management.base import BaseCommand

logger: Any

class LoggingBaseCommand(BaseCommand):
    def execute(self, *args: Any, **options: Any) -> None: ...
