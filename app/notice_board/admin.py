"""Django admin customizations."""
import json
from typing import (  # pylint: disable=unused-import
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    Sequence,
)

from django.contrib import admin
from django.db.models import QuerySet  # pylint: disable=unused-import
from django.db.models.fields.related import (  # pylint: disable=unused-import
    RelatedField,
)
from django.http import HttpRequest
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from common.json_field import JSONField
from crowd.models import User
from notice_board.models import Guild, GuildMember, Meeting, Sphere

with open("app/chronology/json_schema/festival-settings.json", "r") as schema_fd:
    SETTINGS_JSON_SCHEMA = json.loads(schema_fd.read())

if TYPE_CHECKING:
    _BASE = admin.ModelAdmin
else:
    _BASE = object


class SphereManagersAdminMixin(_BASE):
    """Limits queryset by sphere manager."""

    permission_keys = {
        "AgendaItem": "room__festival__sphere__managers",
        "Festival": "sphere__managers",
        "Guild": "*",
        "Helper": "festival__sphere__managers",
        "Meeting": "sphere__managers",
        "Proposal": "waitlist__festival__sphere__managers",
        "Room": "festival__sphere__managers",
        "Site": "sphere__managers",
        "Sphere": "managers",
        "TimeSlot": "festival__sphere__managers",
        "User": "*",
        "WaitList": "festival__sphere__managers",
    }

    def get_list_display(self, request: HttpRequest) -> List[str]:
        list_display = super().get_list_display(request)
        return ["id"] + list(list_display)

    def get_list_display_links(
        self, request: HttpRequest, list_display: Sequence[str]
    ) -> List[str]:
        list_display_links = super().get_list_display_links(request, list_display)
        list_display_links = list(list_display_links or [])
        print(list_display_links)
        if list_display[1] not in list_display_links:
            list_display_links.append(list_display[1])
        return list_display_links

    def get_queryset(self, request: HttpRequest) -> "QuerySet[Any]":
        """Limit querset to show only spheres that user is managing."""
        queryset = super().get_queryset(request)

        return self._get_queryset(request.user, queryset, self.model.__name__)

    def get_field_queryset(
        self,
        db: None,
        db_field: "RelatedField[Any, Any]",
        request: Optional[HttpRequest],
    ) -> "Optional[QuerySet[Any]]":
        queryset = super().get_field_queryset(db, db_field, request)

        if queryset is None:
            queryset = db_field.remote_field.model.objects.all()

        if request is None:
            return queryset

        return self._get_queryset(
            request.user, queryset, db_field.remote_field.model.__name__
        )

    def _get_queryset(
        self, user: User, queryset: "QuerySet[Any]", model_name: str
    ) -> "QuerySet[Any]":
        if not user.is_superuser:
            key = self.permission_keys[model_name]
            if key and key != "*":
                return queryset.filter(**{key: user})
        return queryset


class GuildMemberInline(admin.TabularInline):
    fields = ("user", "membership_type")
    model = GuildMember


class GuildAdmin(admin.ModelAdmin):
    inlines = [GuildMemberInline]
    prepopulated_fields = {"slug": ["name"]}


class MeetingAdmin(SphereManagersAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (
            "Basic info",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                    "sphere",
                    "guild",
                    "organizer",
                    "image",
                )
            },
        ),
        ("Location", {"fields": ("location", "meeting_url",)}),
        ("Time", {"fields": ("start_time", "end_time", "publication_time",)}),
        ("Participants", {"fields": ("participants",)}),
    )
    list_display = (
        "name",
        "status",
        "organizer",
        "created_at",
        "publication_time",
        "start_time",
        "end_time",
        "sphere",
        "guild",
    )
    list_filter = (
        "created_at",
        "status",
        "end_time",
        "guild",
        "publication_time",
        "sphere",
        "start_time",
        "updated_at",
    )
    prepopulated_fields = {"slug": ["name"]}


class SphereAdmin(SphereManagersAdminMixin, SimpleHistoryAdmin):
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditorWidget(options={"schema": SETTINGS_JSON_SCHEMA})
        },
    }
    list_display = ("name", "site", "is_open")
    list_filter = ("is_open",)


admin.site.register(Guild, GuildAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(Meeting, MeetingAdmin)
