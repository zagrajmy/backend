from smtpd import SMTPServer
from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.utils import setup_logger as setup_logger
from django_extensions.management.utils import signalcommand as signalcommand

logger: Any

class ExtensionDebuggingServer(SMTPServer):
    def process_message(
        self, peer: Any, mailfrom: Any, rcpttos: Any, data: Any, **kwargs: Any
    ) -> None: ...

class Command(BaseCommand):
    help: str = ...
    args: str = ...
    requires_system_checks: bool = ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, addrport: str = ..., *args: Any, **options: Any) -> None: ...
