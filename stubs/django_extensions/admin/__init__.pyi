from typing import Any, Callable, Dict, Tuple

from django.contrib import admin
from django_extensions.admin.widgets import (
    ForeignKeySearchInput as ForeignKeySearchInput,
)

class ForeignKeyAutocompleteAdminMixin:
    related_search_fields: Dict[str, Tuple[str]] = ...
    related_string_functions: Dict[str, Callable] = ...
    autocomplete_limit: Any = ...
    def get_urls(self): ...
    def foreignkey_autocomplete(self, request: Any): ...
    def get_related_filter(self, model: Any, request: Any) -> None: ...
    def get_help_text(self, field_name: Any, model_name: Any): ...
    def formfield_for_dbfield(self, db_field: Any, **kwargs: Any): ...

class ForeignKeyAutocompleteAdmin(
    ForeignKeyAutocompleteAdminMixin, admin.ModelAdmin
): ...
class ForeignKeyAutocompleteTabularInline(
    ForeignKeyAutocompleteAdminMixin, admin.TabularInline
): ...
class ForeignKeyAutocompleteStackedInline(
    ForeignKeyAutocompleteAdminMixin, admin.StackedInline
): ...
