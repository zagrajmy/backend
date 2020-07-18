from typing import Any

from django.core.management.base import BaseCommand

from ... import models as models
from ... import utils as utils
from ...exceptions import NotHistoricalModelError as NotHistoricalModelError

get_model: Any

class Command(BaseCommand):
    args: str = ...
    help: str = ...
    COMMAND_HINT: str = ...
    MODEL_NOT_FOUND: str = ...
    MODEL_NOT_HISTORICAL: str = ...
    NO_REGISTERED_MODELS: str = ...
    START_SAVING_FOR_MODEL: str = ...
    DONE_SAVING_FOR_MODEL: str = ...
    EXISTING_HISTORY_FOUND: str = ...
    INVALID_MODEL_ARG: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    verbosity: Any = ...
    def handle(self, *args: Any, **options: Any) -> None: ...
