from django.db import models
from django.contrib.postgres.fields import JSONField

from crowd.models import User
from django.contrib.sites.models import Site


class DescribedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="", blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Guild(DescribedModel):
    """Small group of users for a small club or team."""

    is_public = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through="GuildMember")

    class Meta:  # noqa D106
        db_table = "nb_guild"


class GuildMember(models.Model):
    """Membership model for guilds."""

    APPLIED = "applied"
    MEMBER = "member"
    ADMIN = "admin"
    MEMBERSHIP_TYPES = ((APPLIED, "Applied"), (MEMBER, "Member"), (ADMIN, "Admin"))

    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=255, choices=MEMBERSHIP_TYPES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:  # noqa D106
        db_table = "nb_guild_user"


class Sphere(models.Model):
    """Big group for whole provinces, topics, organizations or big events."""

    is_open = models.BooleanField(default=True)
    managers = models.ManyToManyField(User)
    name = models.CharField(max_length=255)
    settings = JSONField(null=True)
    site = models.OneToOneField(Site, on_delete=models.PROTECT, null=True)

    class Meta:  # noqa D106
        db_table = "nb_sphere"

    def __str__(self) -> str:
        return self.name


class Meeting(DescribedModel):
    """Meeting model."""

    end_time = models.DateTimeField(null=True)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    location = models.TextField(blank=True, null=True)
    meeting_url = models.URLField(blank=True)
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_meetings"
    )
    participants = models.ManyToManyField(User, related_name="participated_meetings")
    publication_time = models.DateTimeField(null=True)
    sphere = models.ForeignKey("Sphere", on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)

    class Meta:  # noqa D106
        db_table = "nb_meeting"

    def __str__(self) -> str:
        return self.title
