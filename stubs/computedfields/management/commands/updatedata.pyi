from typing import Any

from computedfields.models import active_resolver as active_resolver
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help: str = ...
    def handle(self, *args: Any, **options: Any) -> None: ...
