from typing import Dict, TypedDict

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.json_field import JSONField
from crowd.models import User
from notice_board.models import Meeting, Sphere


class EmptyDict(TypedDict):
    pass


def default_festival_settings() -> Dict[str, EmptyDict]:
    return {"theme": {}, "forms": {}}


class Festival(models.Model):
    end_time = models.DateTimeField(verbose_name=_("end time"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    settings = JSONField(default=default_festival_settings, verbose_name=_("settings"))
    slug = models.SlugField(blank=True, verbose_name=_("slug"))
    sphere = models.ForeignKey(
        Sphere, on_delete=models.CASCADE, verbose_name=_("sphere")
    )
    start_proposal = models.DateTimeField(verbose_name=_("start proposal"))
    start_publication = models.DateTimeField(verbose_name=_("start publication"))
    start_time = models.DateTimeField(verbose_name=_("start time"))

    class Meta:
        db_table = "ch_festival"
        verbose_name = _("festival")
        verbose_name_plural = _("festivals")

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, verbose_name=_("festival")
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))

    class Meta:
        db_table = "ch_room"
        verbose_name = _("room")
        verbose_name_plural = _("rooms")

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"


class TimeSlot(models.Model):
    end_time = models.DateTimeField(verbose_name=_("end time"))
    start_time = models.DateTimeField(verbose_name=_("start time"))
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, verbose_name=_("festival")
    )

    class Meta:
        db_table = "ch_time_slot"
        verbose_name = _("time slot")
        verbose_name_plural = _("time slots")

    def __str__(self) -> str:
        return f"From {self.start_time} to {self.end_time} ({self.id})"


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

    def __str__(self) -> str:
        return str(self.user)


class AgendaItem(models.Model):
    helper = models.ForeignKey(
        Helper, on_delete=models.SET_NULL, null=True, verbose_name=_("helper")
    )
    helper_confirmed = models.BooleanField(
        default=False, verbose_name=_("helper confirmed")
    )
    meeting = models.OneToOneField(
        Meeting, on_delete=models.SET_NULL, null=True, verbose_name=_("meeting")
    )
    meeting_confirmed = models.BooleanField(
        default=False, verbose_name=_("meeting confirmed")
    )
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, verbose_name=_("room")
    )

    class Meta:
        db_table = "ch_agenda_item"
        verbose_name = _("agenda item")
        verbose_name_plural = _("agenda items")


class WaitList(models.Model):
    festival = models.ForeignKey(
        Festival, on_delete=models.CASCADE, verbose_name=_("festival")
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))

    class Meta:
        db_table = "ch_wait_list"
        verbose_name = _("waitlist")
        verbose_name_plural = _("waitlists")

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"


def default_json_field() -> EmptyDict:
    return {}


class Proposal(models.Model):
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
        max_length=255, blank=True, null=True, verbose_name=_("city")
    )
    club = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("club")
    )
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=CREATED, verbose_name=_("status")
    )
    meeting = models.OneToOneField(
        Meeting, on_delete=models.CASCADE, null=True, verbose_name=_("meeting")
    )
    needs = models.TextField(blank=True, null=True, verbose_name=_("needs"))
    other_contact = JSONField(
        null=True, default=default_json_field, verbose_name=_("other contact")
    )
    other_data = JSONField(
        null=True, default=default_json_field, verbose_name=_("other data")
    )
    phone = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("phone")
    )
    time_slots = models.ManyToManyField(TimeSlot, verbose_name=_("time slots"))
    waitlist = models.ForeignKey(
        WaitList, on_delete=models.CASCADE, verbose_name=_("waitlist")
    )
    speaker_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="proposals",
        null=True,
        verbose_name=_("speaker user"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name=_("created at")
    )
    speaker_name = models.CharField(max_length=255, verbose_name=_("speaker name"))

    class Meta:
        db_table = "ch_proposal"
        verbose_name = _("proposal")
        verbose_name_plural = _("proposals")

    def __str__(self) -> str:
        return self.name
