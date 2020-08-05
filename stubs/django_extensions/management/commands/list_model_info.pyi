from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.color import color_style as color_style
from django_extensions.management.utils import signalcommand as signalcommand

TAB: str
HALFTAB: str

class Command(BaseCommand):
    help: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def list_model_info(self, options: Any): ...
    def handle(self, *args: Any, **options: Any) -> None: ...
