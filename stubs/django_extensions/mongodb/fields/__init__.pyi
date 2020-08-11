from typing import Any, Optional

from mongoengine.fields import DateTimeField, StringField

class SlugField(StringField):
    description: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_internal_type(self): ...
    def formfield(self, **kwargs: Any): ...

class AutoSlugField(SlugField):
    slugify_function: Any = ...
    separator: Any = ...
    overwrite: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def slugify_func(self, content: Any): ...
    def create_slug(self, model_instance: Any, add: Any): ...
    def get_slug_fields(self, model_instance: Any, lookup_value: Any): ...
    def pre_save(self, model_instance: Any, add: Any): ...
    def get_internal_type(self): ...

class CreationDateTimeField(DateTimeField):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_internal_type(self): ...

class ModificationDateTimeField(CreationDateTimeField):
    def pre_save(self, model: Any, add: Any): ...
    def get_internal_type(self): ...

class UUIDVersionError(Exception): ...

class UUIDField(StringField):
    auto: Any = ...
    version: Any = ...
    def __init__(
        self,
        verbose_name: Optional[Any] = ...,
        name: Optional[Any] = ...,
        auto: bool = ...,
        version: int = ...,
        node: Optional[Any] = ...,
        clock_seq: Optional[Any] = ...,
        namespace: Optional[Any] = ...,
        **kwargs: Any,
    ) -> None: ...
    def get_internal_type(self): ...
    def contribute_to_class(self, cls: Any, name: Any) -> None: ...
    def create_uuid(self): ...
    def pre_save(self, model_instance: Any, add: Any): ...