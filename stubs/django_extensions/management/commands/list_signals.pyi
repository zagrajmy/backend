from typing import Any

from django.core.management.base import BaseCommand

MSG: str
SIGNAL_NAMES: Any

class Command(BaseCommand):
    help: str = ...
    def handle(self, *args: Any, **options: Any): ...
