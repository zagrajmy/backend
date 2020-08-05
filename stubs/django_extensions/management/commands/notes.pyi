from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.compat import get_template_setting as get_template_setting
from django_extensions.management.utils import signalcommand as signalcommand

ANNOTATION_RE: Any
ANNOTATION_END_RE: Any

class Command(BaseCommand):
    help: str = ...
    label: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, *args: Any, **options: Any): ...
