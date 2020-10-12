from __future__ import annotations

from typing import Collection, Dict, Iterable, List, Optional, TypedDict, Union

from computedfields.models import ComputedFieldsModel, computed
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, JSONField, Q, QuerySet  # type: ignore[attr-defined]
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from crowd.models import User
from notice_board.models import Meeting, Sphere


def default_festival_settings() -> Dict[str, Union[List[str], Dict[str, str]]]:
    return {"theme": {}, "forms": []}


class Festival(ComputedFieldsModel):

    DRAFT = "draft"
    READY = "ready"
    PROPOSAL = "proposal"
    AGENDA = "agenda"
    AGENDA_PROPOSAL = "agenda_proposal"
    ONGOING = "ongoing"
    PAST = "past"
    STATUS_CHOICES = (
        (DRAFT, _("draft")),
        (READY, _("ready")),
        (PROPOSAL, _("proposal")),
        (AGENDA, _("agenda")),
        (ONGOING, _("ongoing")),
        (PAST, _("past")),
    )

    start_time = models.DateTimeField(
        blank=True, null=True, verbose_name=_("start time")
    )
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_("end time"))
    history = HistoricalRecords(
        table_name="ch_festival_history",
        history_change_reason_field=models.TextField(null=True),
        bases=[ComputedFieldsModel],
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    settings = JSONField(default=default_festival_settings, verbose_name=_("settings"))
    slug = models.SlugField(verbose_name=_("slug"))
    sphere = models.ForeignKey(
        Sphere, on_delete=models.CASCADE, verbose_name=_("sphere")
    )
    start_proposal = models.DateTimeField(
        blank=True, null=True, verbose_name=_("start proposal")
    )
    end_proposal = models.DateTimeField(
        blank=True, null=True, verbose_name=_("end proposal")
    )
    start_publication = models.DateTimeField(
        blank=True, null=True, verbose_name=_("start publication")
    )

    class Meta:
        db_table = "ch_festival"
        verbose_name = _("festival")
        verbose_name_plural = _("festivals")
        constraints = [
            models.UniqueConstraint(
                fields=("sphere", "slug"), name="festival_has_unique_slug_and_sphere"
            ),
            models.CheckConstraint(
                check=Q(
                    start_proposal__isnull=True,
                    end_proposal__isnull=True,
                    start_publication__isnull=True,
                    start_time__isnull=True,
                    end_time__isnull=True,
                )
                | Q(
                    start_proposal__lte=F("end_proposal"),
                    start_publication__lte=F("start_time"),
                    start_time__lt=F("end_time"),
                ),
                name="festival_date_times",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    @computed(
        models.CharField(max_length=255, choices=STATUS_CHOICES, default=DRAFT),
        depends=[
            ["self", ["start_proposal", "start_publication", "start_time", "end_time"]]
        ],
    )
    def status(self) -> str:
        if (
            self.start_time
            and self.end_time
            and self.start_proposal
            and self.end_proposal
            and self.start_publication
        ):
            now = timezone.now()
            status_mapping = (
                (self.start_proposal, Festival.READY),
                (self.start_publication, Festival.PROPOSAL),
                (self.end_proposal, Festival.AGENDA_PROPOSAL),
                (self.start_time, Festival.AGENDA),
                (self.end_time, Festival.ONGOING),
            )
            for key, value in status_mapping:
                if now < key:
                    return value
            return Festival.PAST
        return Festival.DRAFT

    def agenda_items(self) -> QuerySet[AgendaItem]:
        return AgendaItem.objects.filter(room__festival=self)


class Room(models.Model):
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        verbose_name=_("festival"),
        related_name="rooms",
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))

    class Meta:
        db_table = "ch_room"
        verbose_name = _("room")
        verbose_name_plural = _("rooms")
        constraints = [
            models.UniqueConstraint(
                fields=("slug", "festival"), name="room_has_unique_slug_and_festival"
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"


class TimeSlot(models.Model):  # type: ignore[misc]
    end_time = models.DateTimeField(verbose_name=_("end time"))
    start_time = models.DateTimeField(verbose_name=_("start time"))
    festival = models.ForeignKey(
        Festival,
        on_delete=models.CASCADE,
        verbose_name=_("festival"),
        related_name="time_slots",
    )

    class Meta:
        db_table = "ch_time_slot"
        verbose_name = _("time slot")
        verbose_name_plural = _("time slots")
        constraints = [
            models.UniqueConstraint(
                fields=("festival", "start_time", "end_time"),
                name="timeslot_has_unique_times_for_festival",
            ),
            models.CheckConstraint(
                check=Q(start_time__lt=F("end_time")), name="timeslot_date_times"
            ),
        ]

    def __str__(self) -> str:
        ts_format = "%Y-%m-%d %H:%M"
        start = localtime(self.start_time).strftime(ts_format)
        if self.start_time.date() == self.end_time.date():
            ts_format = "%H:%M"
        end = localtime(self.end_time).strftime(ts_format)
        return f"{start} - {end} ({self.id})"

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[str] = None,
        update_fields: Optional[Iterable[str]] = None,
    ) -> None:
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    def validate_unique(self, exclude: Optional[Collection[str]] = None) -> None:
        super().validate_unique(exclude)
        festival_slots = TimeSlot.objects.filter(festival=self.festival)
        conflicted = festival_slots.filter(
            Q(start_time__gt=self.start_time, start_time__lt=self.end_time)
            | Q(end_time__gt=self.start_time, end_time__lt=self.end_time)
            | Q(start_time__lte=self.start_time, end_time__gte=self.end_time)
        ).last()
        if conflicted and conflicted != self:
            raise ValidationError(_("Time slots can't overlap!"))


class Helper(models.Model):
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, verbose_name=_("festival")
    )
    time_slots = models.ManyToManyField(TimeSlot, verbose_name=_("time slots"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))

    class Meta:
        db_table = "ch_helper"
        verbose_name = _("helper")
        verbose_name_plural = _("helpers")
        constraints = [
            models.UniqueConstraint(
                fields=("festival", "user"), name="helper_has_unique_user_and_festival"
            )
        ]

    def __str__(self) -> str:
        return str(self.user)


class AgendaItem(ComputedFieldsModel):
    UNASSIGNED = "unassigned"
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    STATUS_CHOICES = (
        (UNASSIGNED, _("unassigned")),
        (UNCONFIRMED, _("unconfirmed")),
        (CONFIRMED, _("confirmed")),
    )

    helper = models.ForeignKey(
        Helper,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("helper"),
    )
    helper_confirmed = models.BooleanField(
        default=False, verbose_name=_("helper confirmed")
    )
    meeting = models.OneToOneField(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name=_("meeting"),
        related_name="agenda_item",
    )
    meeting_confirmed = models.BooleanField(
        default=False, verbose_name=_("meeting confirmed")
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name=_("room"),
        related_name="agenda_item",
    )

    class Meta:
        db_table = "ch_agenda_item"
        verbose_name = _("agenda item")
        verbose_name_plural = _("agenda items")

    @computed(
        models.CharField(max_length=255, choices=STATUS_CHOICES, default=UNASSIGNED),
        depends=[
            ["self", ["helper", "helper_confirmed", "meeting", "meeting_confirmed"]]
        ],
    )
    def status(self) -> str:
        if not self.helper:
            return AgendaItem.UNASSIGNED

        if self.meeting_confirmed and self.helper_confirmed:
            return AgendaItem.CONFIRMED
        return AgendaItem.UNCONFIRMED

    def __str__(self) -> str:
        return (
            # pylint: disable=no-member
            f"{self.meeting.name} by {self.meeting.proposal.speaker_name} "
            f"({self.status})"
        )


class WaitList(models.Model):
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, verbose_name=_("festival")
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))

    class Meta:
        db_table = "ch_wait_list"
        verbose_name = _("waitlist")
        verbose_name_plural = _("waitlists")
        constraints = [
            models.UniqueConstraint(
                fields=("slug", "festival"),
                name="waitlist_has_unique_slug_and_festival",
            )
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"


class EmptyDict(TypedDict):
    pass


def default_json_field() -> EmptyDict:
    return {}


class Proposal(models.Model):  # type: ignore[misc]
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    STATUS_CHOICES = (
        (CREATED, _("Created")),
        (ACCEPTED, _("Accepted")),
        (REJECTED, _("Rejected")),
    )

    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(
        default="", blank=True, verbose_name=_("description")
    )
    duration_minutes = models.PositiveIntegerField(verbose_name=_("duration minutes"))
    city = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("city")
    )
    club = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("club")
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=CREATED, verbose_name=_("status")
    )
    meeting = models.OneToOneField(
        Meeting,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("meeting"),
        related_name="proposal",
    )
    needs = models.TextField(default="", blank=True, verbose_name=_("needs"))
    other_contact = JSONField(
        blank=True, default=default_json_field, verbose_name=_("other contact")
    )
    other_data = JSONField(
        blank=True, default=default_json_field, verbose_name=_("other data")
    )
    phone = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("phone")
    )
    time_slots = models.ManyToManyField(TimeSlot, verbose_name=_("time slots"))
    waitlist = models.ForeignKey(
        WaitList, on_delete=models.CASCADE, verbose_name=_("waitlist")
    )
    speaker_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="proposals",
        blank=True,
        null=True,
        verbose_name=_("speaker user"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    speaker_name = models.CharField(max_length=255, verbose_name=_("speaker name"))
    topic = models.CharField(
        max_length=255, default="", blank=True, verbose_name=_("topic")
    )

    class Meta:
        db_table = "ch_proposal"
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def __str__(self) -> str:
        return self.name
