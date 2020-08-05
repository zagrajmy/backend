from typing import Any

from django_extensions.collision_resolvers import (
    CollisionResolvingRunner as CollisionResolvingRunner,
)
from django_extensions.import_subclasses import SubclassesFinder as SubclassesFinder
from django_extensions.utils.deprecation import (
    RemovedInNextVersionWarning as RemovedInNextVersionWarning,
)

SHELL_PLUS_DJANGO_IMPORTS: Any

class ObjectImportError(Exception): ...

def get_app_name(mod_name: Any): ...
def import_items(import_directives: Any, style: Any, quiet_load: bool = ...): ...
def import_objects(options: Any, style: Any): ...
