from typing import Any, Optional

from django.contrib import admin

from .graph import ComputedModelsGraph as ComputedModelsGraph
from .models import ComputedFieldsAdminModel as ComputedFieldsAdminModel
from .models import ContributingModelsModel as ContributingModelsModel
from .resolver import active_resolver as active_resolver

class ComputedModelsAdmin(admin.ModelAdmin):
    actions: Any = ...
    change_list_template: str = ...
    list_display: Any = ...
    list_display_links: Any = ...
    def has_add_permission(self, request: Any): ...
    def has_delete_permission(self, request: Any, obj: Optional[Any] = ...): ...
    def dependencies(self, inst: Any): ...
    def computed_fields(self, inst: Any): ...
    def local_computed_fields_mro(self, inst: Any): ...
    def name(self, obj: Any): ...
    def get_urls(self): ...
    def modelgraph(self, inst: Any): ...
    def render_graph(self, request: Any, extra_context: Optional[Any] = ...): ...
    def render_uniongraph(self, request: Any, extra_context: Optional[Any] = ...): ...
    def render_modelgraph(
        self, request: Any, modelid: Any, extra_context: Optional[Any] = ...
    ): ...

class ContributingModelsAdmin(admin.ModelAdmin):
    actions: Any = ...
    list_display: Any = ...
    list_display_links: Any = ...
    def has_add_permission(self, request: Any): ...
    def has_delete_permission(self, request: Any, obj: Optional[Any] = ...): ...
    def fk_fields(self, inst: Any): ...
    def name(self, obj: Any): ...