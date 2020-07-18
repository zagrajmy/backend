from typing import Any

from ... import models as models
from ... import utils as utils
from ...exceptions import NotHistoricalModelError as NotHistoricalModelError
from . import populate_history as populate_history

class Command(populate_history.Command):
    args: str = ...
    help: str = ...
    DONE_CLEANING_FOR_MODEL: str = ...
    def add_arguments(self, parser: Any) -> None: ...
    verbosity: Any = ...
    def handle(self, *args: Any, **options: Any) -> None: ...
    def log(self, message: Any, verbosity_level: int = ...) -> None: ...
