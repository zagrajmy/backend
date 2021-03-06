from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.utils import signalcommand as signalcommand

USE_STATICFILES: Any

class KCacheGrind:
    data: Any = ...
    out_file: Any = ...
    def __init__(self, profiler: Any) -> None: ...
    def output(self, out_file: Any) -> None: ...

class Command(BaseCommand):
    help: str = ...
    args: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, addrport: str = ..., *args: Any, **options: Any): ...
