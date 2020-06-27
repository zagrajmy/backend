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
        JSONField: {"widget": JSONEditorWidget},
    }
    inlines = (
        WaitListInline,
        TimeSlotInline,
        RoomInline,
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


class ProposalTimeSlotInline(admin.TabularInline):
    model = Proposal.time_slots.through


class ProposalAdmin(SphereManagersAdmin):
    inlines = [ProposalTimeSlotInline]
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }


admin.site.register(AgendaItem, SphereManagersAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Helper, SphereManagersAdmin)
admin.site.register(WaitList, WaitListAdmin)
