from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.color import color_style as color_style
from django_extensions.management.utils import signalcommand as signalcommand

HAS_REQUESTS: bool

class Command(BaseCommand):
    help: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    style: Any = ...
    options: Any = ...
    reqs: Any = ...
    github_api_token: Any = ...
    def handle(self, *args: Any, **options: Any) -> None: ...
    def check_pypi(self) -> None: ...
    def check_github(self) -> None: ...
    def check_other(self) -> None: ...