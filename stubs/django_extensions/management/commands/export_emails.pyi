from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.utils import signalcommand as signalcommand

FORMATS: Any

def full_name(**kwargs: Any): ...

class Command(BaseCommand):
    help: str = ...
    args: str = ...
    label: str = ...
    can_import_settings: bool = ...
    encoding: str = ...
    UserModel: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def add_arguments(self, parser: Any) -> None: ...
    def full_name(self, **kwargs: Any): ...
    def handle(self, *args: Any, **options: Any) -> None: ...
    def address(self, qs: Any) -> None: ...
    def emails(self, qs: Any) -> None: ...
    def google(self, qs: Any) -> None: ...
    def linkedin(self, qs: Any) -> None: ...
    def outlook(self, qs: Any) -> None: ...
    def vcard(self, qs: Any) -> None: ...