import json
from typing import Any

from django.contrib import admin
from django.db.models import JSONField
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from chronology.models import (
    AgendaItem,
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    WaitList,
)
from crowd.models import User
from notice_board.admin import SphereManagersAdminMixin
from notice_board.models import Meeting

with open("app/chronology/json_schema/festival-settings.json", "r") as schema_fd:
    SETTINGS_JSON_SCHEMA = json.loads(schema_fd.read())


class WaitListInline(admin.TabularInline):
    model = WaitList

    fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

    fields = ("start_time", "end_time")


class RoomInline(admin.TabularInline):
    model = Room
    prepopulated_fields = {"slug": ["name"]}


class FestivalAdmin(
    SphereManagersAdminMixin[Festival], SimpleHistoryAdmin
):  # pylint: disable=unsubscriptable-object
    fieldsets = (
        ("Basic info", {"fields": ["sphere", "name", "slug", "settings"]}),
        (
            "Time",
            {
                "fields": [
                    "start_proposal",
                    "end_proposal",
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
        "status",
        "start_proposal",
        "end_proposal",
        "start_publication",
        "start_time",
        "end_time",
    )
    list_filter = (
        "sphere",
        "status",
        "start_proposal",
        "end_proposal",
        "start_publication",
        "start_time",
        "end_time",
    )
    prepopulated_fields = {"slug": ["name"]}


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

    def has_add_permission(self, request: HttpRequest, obj: Any) -> bool:
        return False


class WaitListAdmin(
    SphereManagersAdminMixin[WaitList], admin.ModelAdmin
):  # pylint: disable=unsubscriptable-object
    inlines = [ProposalInline]
    list_display = ("name", "slug", "festival")
    list_filter = ("festival",)
    prepopulated_fields = {"slug": ["name"]}


class ProposalTimeSlotInline(admin.TabularInline):
    model = Proposal.time_slots.through


class ProposalAdmin(
    SphereManagersAdminMixin[Proposal], admin.ModelAdmin
):  # pylint: disable=unsubscriptable-object
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
    actions = ["accept_proposals"]

    def accept_proposals(self, request: HttpRequest, queryset: Any) -> None:
        stats = {"total": 0, "accepted": 0, "skipped": 0}
        for proposal in queryset:
            stats["total"] += 1
            if proposal.meeting:
                stats["skipped"] += 1
                continue
            if proposal.speaker_user:
                user = proposal.speaker_user
            else:
                user = User.objects.first()
            meeting = Meeting.objects.create(
                name=proposal.name,
                description=proposal.description,
                organizer=user,
                sphere=proposal.waitlist.festival.sphere,
            )
            proposal.meeting = meeting
            proposal.save()
            stats["accepted"] += 1
        self.message_user(
            request, _("Total processed: %(total)d, accepted: %(accepted)d") % stats
        )

    accept_proposals.short_description = _("Accept Proposals")  # type: ignore


class AgendaItemAdmin(
    SphereManagersAdminMixin[AgendaItem], admin.ModelAdmin
):  # pylint: disable=unsubscriptable-object
    list_display = (
        "room",
        "meeting",
        "helper",
        "meeting_confirmed",
        "helper_confirmed",
        "status",
    )
    list_filter = (
        "room",
        "helper",
        "meeting_confirmed",
        "helper_confirmed",
        "status",
    )
    list_editable = (
        "meeting_confirmed",
        "helper_confirmed",
    )


class HelperAdmin(
    SphereManagersAdminMixin[Helper], admin.ModelAdmin
):  # pylint: disable=unsubscriptable-object
    list_display = ("user",)
    list_filter = ("festival",)


admin.site.register(AgendaItem, AgendaItemAdmin)
admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Festival, FestivalAdmin)
admin.site.register(Helper, HelperAdmin)
admin.site.register(WaitList, WaitListAdmin)
