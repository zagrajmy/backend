from typing import Any, List, Optional, Type

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.urls.resolvers import URLPattern

from . import utils as utils

USER_NATURAL_KEY: Any
SIMPLE_HISTORY_EDIT: Any

class SimpleHistoryAdmin(admin.ModelAdmin):
    object_history_template: str = ...
    object_history_form_template: str = ...
    def get_urls(self) -> List[URLPattern]: ...
    def history_view(
        self, request: Any, object_id: Any, extra_context: Optional[Any] = ...
    ) -> HttpResponse: ...
    def history_view_title(self, obj: Any) -> str: ...
    def response_change(self, request: Any, obj: Any) -> HttpResponseRedirect: ...
    def history_form_view(
        self,
        request: Any,
        object_id: Any,
        version_id: Any,
        extra_context: Optional[Any] = ...,
    ) -> HttpResponse: ...
    def history_form_view_title(self, obj: Any) -> str: ...
    def render_history_view(
        self, request: Any, template: Any, context: Any, **kwargs: Any
    ) -> HttpResponse: ...
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None: ...
    @property
    def content_type_model_cls(self) -> Type[ContentType]: ...
    @property
    def revert_disabled(self) -> bool: ...