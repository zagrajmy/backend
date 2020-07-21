from typing import Dict, TypedDict

from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from common.json_field import JSONField
from crowd.models import User


class DescribedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    description = models.TextField(
        default="", blank=True, verbose_name=_("description")
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    slug = models.SlugField(verbose_name=_("slug"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Guild(DescribedModel):
    """Small group of users for a small club or team."""

    is_public = models.BooleanField(default=True, verbose_name=_("is public"))
    members = models.ManyToManyField(
        User, through="GuildMember", verbose_name=_("members")
    )

    class Meta:  # noqa D106
        db_table = "nb_guild"
        verbose_name = _("guild")
        verbose_name_plural = _("guilds")


class GuildMember(models.Model):
    """Membership model for guilds."""

    APPLIED = "applied"
    MEMBER = "member"
    ADMIN = "admin"
    MEMBERSHIP_TYPES = (
        (APPLIED, _("Applied")),
        (MEMBER, _("Member")),
        (ADMIN, _("Admin")),
    )

    guild = models.ForeignKey(
        "Guild", on_delete=models.CASCADE, verbose_name=_("guild")
    )
    membership_type = models.CharField(
        max_length=255, choices=MEMBERSHIP_TYPES, verbose_name=_("membership type")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("user"))

    class Meta:  # noqa D106
        db_table = "nb_guild_member"
        verbose_name = _("guild member")
        verbose_name_plural = _("guild members")


class EmptyDict(TypedDict):
    pass


def default_sphere_settings() -> Dict[str, EmptyDict]:
    return {"theme": {}}


class Sphere(models.Model):
    """Big group for whole provinces, topics, organizations or big events."""

    history = HistoricalRecords(
        table_name="nb_sphere_history",
        history_change_reason_field=models.TextField(null=True),
    )
    is_open = models.BooleanField(default=True, verbose_name=_("is open"))
    managers = models.ManyToManyField(User, verbose_name=_("managers"))
    name = models.CharField(max_length=255, verbose_name=_("name"))
    settings = JSONField(default=default_sphere_settings)
    site = models.OneToOneField(
        Site, on_delete=models.PROTECT, related_name="sphere", verbose_name=_("site"),
    )

    class Meta:  # noqa D106
        db_table = "nb_sphere"
        verbose_name = _("sphere")
        verbose_name_plural = _("spheres")

    def __str__(self) -> str:
        return self.name


class Meeting(DescribedModel):
    """Meeting model."""

    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_("end time"))
    guild = models.ForeignKey(
        "Guild",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("guild"),
    )
    image = models.ImageField(null=True, blank=True, verbose_name=_("image"))
    location = models.TextField(blank=True, default="", verbose_name=_("location"))
    meeting_url = models.URLField(blank=True, verbose_name=_("meeting url"))
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_meetings",
        verbose_name=_("organizer"),
    )
    participants = models.ManyToManyField(
        User, related_name="participated_meetings", verbose_name=_("participants")
    )
    publication_time = models.DateTimeField(
        blank=True, null=True, verbose_name=_("publication time")
    )
    sphere = models.ForeignKey(
        "Sphere", on_delete=models.CASCADE, verbose_name=_("sphere")
    )
    start_time = models.DateTimeField(
        blank=True, null=True, verbose_name=_("start time")
    )

    class Meta:  # noqa D106
        db_table = "nb_meeting"
        verbose_name = _("meeting")
        verbose_name_plural = _("meetings")
