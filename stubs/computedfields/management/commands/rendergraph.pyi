from typing import Any

from computedfields.graph import ComputedModelsGraph as ComputedModelsGraph
from computedfields.graph import CycleException as CycleException
from computedfields.models import active_resolver as active_resolver
from django.core.management.base import BaseCommand

COLORS: Any
LEGEND: str

class Command(BaseCommand):
    help: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...
