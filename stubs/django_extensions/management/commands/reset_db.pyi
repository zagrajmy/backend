from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.mysql import parse_mysql_cnf as parse_mysql_cnf
from django_extensions.management.utils import signalcommand as signalcommand
from django_extensions.settings import MYSQL_ENGINES as MYSQL_ENGINES
from django_extensions.settings import POSTGRESQL_ENGINES as POSTGRESQL_ENGINES
from django_extensions.settings import SQLITE_ENGINES as SQLITE_ENGINES

class Command(BaseCommand):
    help: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...
