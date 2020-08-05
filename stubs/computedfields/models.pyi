from typing import Any, Callable, List, Optional, TypeVar

from django.contrib.contenttypes.models import ContentType
from django.db import models

from .resolver import _ComputedFieldsModelBase
from .resolver import active_resolver as active_resolver

class ComputedFieldsModel(_ComputedFieldsModelBase, models.Model):
    class Meta:
        abstract: bool = ...
    def save(
        self,
        force_insert: bool = ...,
        force_update: bool = ...,
        using: Optional[Any] = ...,
        update_fields: Optional[Any] = ...,
        skip_computedfields: bool = ...,
    ) -> Any: ...

X = TypeVar("X")
Y = TypeVar("Y")
M = TypeVar("M", bound=models.Model)

def computed(
    field: models.Field[X, Y],
    depends: Optional[List[List[Any]]] = None,
    select_related: Optional[List[str]] = None,
    prefetch_related: Optional[List[str]] = None,
) -> Callable[[Callable[[M], X]], models.Field[X, Y]]: ...

precomputed: Any
compute: Any
update_computedfields: Any
update_dependent: Any
update_dependent_multi: Any
preupdate_dependent: Any
preupdate_dependent_multi: Any
has_computedfields: Any
is_computedfield: Any
get_contributing_fks: Any

class ComputedModelManager(models.Manager[M]):
    def get_queryset(self) -> models.QuerySet[M]: ...

class ComputedFieldsAdminModel(ContentType):
    objects: Any = ...
    class Meta:
        proxy: bool = ...
        managed: bool = ...
        verbose_name: Any = ...
        verbose_name_plural: Any = ...
        ordering: Any = ...

class ModelsWithContributingFkFieldsManager(models.Manager[M]):
    def get_queryset(self) -> models.QuerySet[M]: ...

class ContributingModelsModel(ContentType):
    objects: Any = ...
    class Meta:
        proxy: bool = ...
        managed: bool = ...
        verbose_name: Any = ...
        verbose_name_plural: Any = ...
        ordering: Any = ...
