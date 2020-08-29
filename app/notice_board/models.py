from typing import Any, Dict

from computedfields.models import ComputedFieldsModel, computed
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import F, JSONField, Q
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

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

    @classmethod
    def _get_unique_slug(cls, name: str, **unique_within: Any) -> str:
        base_slug = str(slugify(name))[:48]
        slug = base_slug
        i = 1
        while cls.objects.filter(slug=slug, **unique_within).exists():
            slug = f"{base_slug}-{i}"
            i += 1
        return slug

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = self._get_unique_slug(self.name)
        super().save(force_insert, force_update, using, update_fields)


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
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="guild_unique_slug")
        ]


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
        constraints = [
            models.UniqueConstraint(
                fields=["guild", "user"], name="guildmember_unique_guild_and_user"
            )
        ]


def default_sphere_settings() -> Dict[str, Any]:
    return {"theme": {}, "forms": []}


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


class Meeting(DescribedModel, ComputedFieldsModel):
    """Meeting model."""

    DRAFT = "draft"
    PLANNED = "planned"
    PUBLISHED = "published"
    ONGOING = "ongoing"
    PAST = "past"
    STATUS_CHOICES = (
        (DRAFT, _("draft")),
        (PLANNED, _("planned")),
        (PUBLISHED, _("published")),
        (ONGOING, _("ongoing")),
        (PAST, _("past")),
    )

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
        User,
        related_name="participated_meetings",
        verbose_name=_("participants"),
        through="MeetingParticipant",
    )
    participants_limit = models.IntegerField(
        default=0, verbose_name=_("participants limit")
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
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "guild"],
                condition=models.Q(guild__isnull=False),
                name="meeting_unique_slug_in_guild",
            ),
            models.UniqueConstraint(
                fields=["slug", "sphere"],
                condition=models.Q(guild__isnull=True),
                name="meeting_unique_slug_in_sphere",
            ),
            models.CheckConstraint(
                check=Q(
                    publication_time__isnull=True,
                    start_time__isnull=True,
                    end_time__isnull=True,
                )
                | Q(
                    created_at__lte=F("publication_time"),
                    publication_time__lte=F("start_time"),
                    start_time__lt=F("end_time"),
                ),
                name="meeting_date_times",
            ),
        ]

    @computed(
        models.CharField(max_length=255, choices=STATUS_CHOICES, default=DRAFT),
        depends=[["self", ["start_time", "end_time", "publication_time"]]],
    )
    def status(self) -> str:
        now = timezone.now()
        if not self.start_time or not self.end_time or not self.publication_time:
            return Meeting.DRAFT
        if now < self.publication_time:
            return Meeting.PLANNED
        if now < self.start_time:
            return Meeting.PUBLISHED
        if now < self.end_time:
            return Meeting.ONGOING
        return Meeting.PAST

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = self._get_unique_slug(self.name, sphere=self.sphere)
        super().save(force_insert, force_update, using, update_fields)


class MeetingParticipant(models.Model):
    class Meta:
        unique_together = [
            ("meeting", "user"),
        ]
        db_table = "nb_meeting_participant"

    CONFIRMED = "CONFIRMED"
    WAITING = "WAITING"
    CONFIRM_CHOICES = [
        (CONFIRMED, "Confirmed"),
        (WAITING, "Waiting"),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    meeting = models.ForeignKey(Meeting, models.CASCADE)
    status = models.CharField(max_length=15, choices=CONFIRM_CHOICES)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))
    user = models.ForeignKey(User, models.CASCADE)
