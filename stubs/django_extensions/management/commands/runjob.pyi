from typing import Any

from django.core.management.base import BaseCommand
from django_extensions.management.jobs import get_job as get_job
from django_extensions.management.jobs import print_jobs as print_jobs
from django_extensions.management.utils import setup_logger as setup_logger
from django_extensions.management.utils import signalcommand as signalcommand

logger: Any

class Command(BaseCommand):
    help: str = ...
    missing_args_message: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    def runjob(self, app_name: Any, job_name: Any, options: Any) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...