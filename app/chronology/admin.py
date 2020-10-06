from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, TypeVar

import pytz
from django.contrib.admin import ModelAdmin, TabularInline, site
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.db.models import JSONField, Model, Q, QuerySet
from django.db.models.fields.related import RelatedField
from django.forms import CharField, Form, ModelForm
from django.forms.widgets import HiddenInput
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path
from django.urls.resolvers import URLPattern
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django_json_widget.widgets import JSONEditorWidget
from simple_history.admin import SimpleHistoryAdmin

from notice_board.admin import SphereManagersAdminMixin
from notice_board.models import Meeting

from .agenda_builder import AgendaBuilder
from .models import AgendaItem, Festival, Helper, Proposal, Room, TimeSlot, WaitList

ModelVar = TypeVar("ModelVar", bound=Model)

with open("app/chronology/json_schema/festival-settings.json", "r") as schema_fd:
    SETTINGS_JSON_SCHEMA = json.loads(schema_fd.read())


URL_HOUR_FORMAT = "%Y-%m-%d-%H-%M-%S-%f-%Z"


def strphour(hour: str) -> datetime:
    return make_aware(
        datetime.strptime(hour, URL_HOUR_FORMAT),
        pytz.UTC,
    )


class WaitListInline(TabularInline):
    model = WaitList

    fields = ("name", "slug")
    prepopulated_fields = {"slug": ["name"]}


class TimeSlotInline(TabularInline):
    model = TimeSlot

    fields = ("start_time", "end_time")


class RoomInline(TabularInline):
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
    change_form_template = "chronology/festival_change.html"
    agenda_builder_class = AgendaBuilder

    def get_urls(self) -> List[URLPattern]:
        urls = super().get_urls()
        my_urls = [
            path(
                "<int:object_id>/agenda/",
                staff_member_required(self.agenda),
                name="chronology_festival_agenda",
            ),
        ]
        return my_urls + urls

    def agenda(self, request: HttpRequest, object_id: int) -> TemplateResponse:
        festival = self.get_queryset(request).get(pk=object_id)
        agenda_builder = FestivalAdmin.agenda_builder_class(
            agenda_items=list(festival.agenda_items()),
            rooms=list(festival.rooms.all()),
            time_slots=list(festival.time_slots.all()),
            unassigned_meetings=list(
                Meeting.objects.filter(
                    agenda_item=None, proposal__waitlist__festival=festival
                )
                .prefetch_related("proposal__time_slots")
                .values("pk", "name", "proposal__time_slots")
            ),
        )
        agenda_builder.build()

        context = dict(
            self.admin_site.each_context(request),
            festival=festival,
            title=_(f"Festival schedule {festival}"),
            agenda_matrix=agenda_builder.agenda_matrix,
            media=self.media,
            broken_agenda_items=agenda_builder.broken_agenda_items,
        )
        return TemplateResponse(request, "chronology/agenda.html", context)


class ProposalInline(TabularInline):
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

    def has_add_permission(self, request: HttpRequest, obj: Proposal) -> bool:
        return False


class WaitListAdmin(
    SphereManagersAdminMixin[WaitList], ModelAdmin
):  # pylint: disable=unsubscriptable-object
    inlines = [ProposalInline]
    list_display = ("name", "slug", "festival")
    list_filter = ("festival",)
    prepopulated_fields = {"slug": ["name"]}


class ProposalTimeSlotInline(TabularInline):
    model = Proposal.time_slots.through


class ProposalAdmin(
    SphereManagersAdminMixin[Proposal], ModelAdmin
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

    def accept_proposals(
        self, request: HttpRequest, queryset: QuerySet[Proposal]
    ) -> None:
        total = queryset.count()

        accepted = 0
        for proposal in queryset.filter(meeting__isnull=True):
            sphere = proposal.waitlist.festival.sphere

            proposal.meeting = Meeting.objects.create(
                description=proposal.description,
                name=proposal.name,
                organizer=proposal.speaker_user or request.user,
                publication_time=proposal.waitlist.festival.start_publication,
                sphere=sphere,
            )
            proposal.save()

            accepted += 1
        self.message_user(request, _(f"Total processed: {total}, accepted: {accepted}"))

    accept_proposals.short_description = _("Accept Proposals")  # type: ignore


class AgendaItemForm(ModelForm):
    hour = CharField(widget=HiddenInput(), required=False)

    class Meta:
        model = AgendaItem
        fields = [
            "helper",
            "helper_confirmed",
            "hour",
            "meeting",
            "meeting_confirmed",
            "room",
        ]

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        start = self._get_hour(cleaned_data.get("hour"))
        proposal = cleaned_data["meeting"].proposal
        end = start + timedelta(minutes=proposal.duration_minutes)
        possible_conflicts = AgendaItem.objects.filter(
            Q(meeting__start_time__gt=start, meeting__start_time__lt=end)
            | Q(meeting__end_time__gt=start, meeting__end_time__lt=end)
            | Q(meeting__start_time__lte=start, meeting__end_time__gte=end)
        ).exclude(id=self.instance.pk)
        conflicted_item = possible_conflicts.filter(room=cleaned_data["room"]).last()
        if conflicted_item and conflicted_item != self.instance:
            raise ValidationError(
                _("There's already an agenda item in this time slot.")
            )
        time_slot = cleaned_data["room"].festival.time_slots.get(
            start_time__lte=start, end_time__gte=start
        )
        if time_slot.end_time < end:
            raise ValidationError(_("Meeting too long for this time slot and hour"))
        user_lookup = {}
        if proposal.speaker_user:
            user_lookup["meeting__proposal__speaker_user"] = proposal.speaker_user
        else:
            user_lookup["meeting__proposal__speaker_name"] = proposal.speaker_name
        users_meetings = possible_conflicts.filter(**user_lookup)
        if users_meetings.exists():
            raise ValidationError(_("User already has a meeting at this hour"))
        if proposal.speaker_user and possible_conflicts.filter(
            helper__user=proposal.speaker_user
        ):
            raise ValidationError(_("User is on helper duty during this time"))
        return cleaned_data

    def _get_hour(self, cleaned_hour: Optional[str]) -> datetime:
        if self.instance and self.instance.pk:
            return self.instance.meeting.start_time

        if cleaned_hour:
            return strphour(cleaned_hour)

        raise ValidationError(_("Missing hour field value"))


class AgendaItemAdmin(
    SphereManagersAdminMixin[AgendaItem], ModelAdmin
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
    form = AgendaItemForm

    def get_field_queryset(
        self,
        db: None,
        db_field: RelatedField[AgendaItem, ModelVar],
        request: Optional[HttpRequest],
    ) -> Optional[QuerySet[ModelVar]]:
        queryset = super().get_field_queryset(db, db_field, request)
        if queryset is not None and request is not None and "_popup" in request.GET:
            return self._filter_popup_queryset(
                db_field.remote_field.model.__name__, queryset, request
            )
        return queryset

    def _filter_popup_queryset(
        self, model_name: str, queryset: QuerySet[ModelVar], request: HttpRequest
    ) -> QuerySet[ModelVar]:

        room = get_object_or_404(
            Room,
            pk=self.get_changeform_initial_data(request)["room"],
        )
        hour = strphour(self.get_changeform_initial_data(request)["hour"])
        filters = {
            "Meeting": (
                Q(
                    agenda_item__isnull=True,
                    proposal__time_slots__start_time__lte=hour,
                    proposal__time_slots__end_time__gte=hour,
                )
                | Q(agenda_item__room=room, start_time=hour)
            )
            & Q(proposal__waitlist__festival=room.festival),
            "Helper": Q(
                festival=room.festival,
                time_slots__start_time__lte=hour,
                time_slots__end_time__gte=hour,
            ),
            "Room": Q(id=room.id),
        }
        return queryset.filter(filters[model_name])

    def save_model(
        self, request: HttpRequest, obj: AgendaItem, form: Form, change: bool
    ) -> None:
        super().save_model(request, obj, form, change)

        start = strphour(self.get_changeform_initial_data(request)["hour"])
        end = start + timedelta(minutes=obj.meeting.proposal.duration_minutes)
        Meeting.objects.filter(id=obj.meeting.id).update(
            start_time=start,
            end_time=end,
            location=obj.room.name,
        )

    def delete_model(self, request: HttpRequest, obj: AgendaItem) -> None:
        Meeting.objects.filter(id=obj.meeting.id).update(
            start_time=None,
            end_time=None,
            location="",
        )

        super().delete_model(request, obj)


class HelperAdmin(
    SphereManagersAdminMixin[Helper], ModelAdmin
):  # pylint: disable=unsubscriptable-object
    list_display = ("user",)
    list_filter = ("festival",)


site.register(AgendaItem, AgendaItemAdmin)
site.register(Festival, FestivalAdmin)
site.register(Helper, HelperAdmin)
site.register(Proposal, ProposalAdmin)
site.register(WaitList, WaitListAdmin)
