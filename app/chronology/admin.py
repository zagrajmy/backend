import json
from typing import Any

from django.contrib import admin
from django.http import HttpRequest
from django_json_widget.widgets import JSONEditorWidget

from chronology.models import (
    AgendaItem,
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    WaitList,
)
from common.json_field import JSONField
from notice_board.admin import SphereManagersAdmin

with open("app/chronology/json_schema/festival-settings.json", "r") as schema_fd:
    SETTINGS_JSON_SCHEMA = json.loads(schema_fd.read())


class WaitListInline(admin.TabularInline):
    model = WaitList

    fields = ("name",)


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

    fields = ("start_time", "end_time")


class RoomInline(admin.TabularInline):
    model = Room


class FestivalAdmin(SphereManagersAdmin):
    fieldsets = (
        ("Basic info", {"fields": ["sphere", "name", "slug", "settings"]}),
        (
            "Time",
            {
                "fields": [
                    "start_proposal",
                    "start_publication",
                    "start_time",
                    "end_time",
                ]
            },
        ),
    )
    formfield_overrides = {
        JSONField: {
            "widget": JSONEditorWidget(options={"schema": SETTINGS_JSON_SCHEMA})
        }
    }
    inlines = (
        WaitListInline,
        TimeSlotInline,
        RoomInline,
    )
    list_display = (
        "name",
        "sphere",
        "start_proposal",
        "start_publication",
        "start_time",
        "end_time",
    )
    list_filter = (
        "sphere",
        "start_proposal",
        "start_publication",
        "start_time",
        "end_time",
    )


class ProposalInline(admin.TabularInline):
    model = Proposal
    can_delete = False
    readonly_fields = (
        "city",
        "club",
        "needs",
        "other_contact",
        "other_data",
        "phone",
        "meeting",
        "time_slots",
    )

    def has_add_permission(  # type: ignore
        self, request: HttpRequest, obj: Any
    ) -> bool:
        return False


class WaitListAdmin(SphereManagersAdmin):
    inlines = [ProposalInline]
    list_display = ("name", "festival")
    list_filter = ("festival",)


class ProposalTimeSlotInline(admin.TabularInline):
    model = Proposal.time_slots.through


class ProposalAdmin(SphereManagersAdmin):
    inlines = [ProposalTimeSlotInline]
    formfield_overrides = {JSONField: {"widget": JSONEditorWidget}}
    list_display = (
        "name",
        "topic",
        "speaker_name",
        "city",
        "club",
        "created_at",
        "duration_minutes",
        "phone",
        "status",
        "waitlist",
    )
    list_filter = (
        "city",
        "club",
        "created_at",
        "duration_minutes",
        "status",
        "waitlist",
    )


class AgendaItemAdmin(SphereManagersAdmin):
    list_display = (
        "room",
        "meeting",
        "helper",
        "meeting_confirmed",
        "helper_confirmed",
    )
    list_filter = (
        "room",
        "helper",
        "meeting_confirmed",
        "helper_confirmed",
    )
    list_editable = (
        "meeting_confirmed",
        "helper_confirmed",
    )


class HelperAdmin(SphereManagersAdmin):
    list_display = ("user",)
    list_filter = ("festival",)


admin.site.register(AgendaItem, AgendaItemAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Helper, HelperAdmin)
admin.site.register(WaitList, WaitListAdmin)
