from typing import Any

from django.apps import AppConfig

from .resolver import BOOT_RESOLVER as BOOT_RESOLVER

class ComputedfieldsConfig(AppConfig):
    name: str = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def ready(self) -> None: ...
