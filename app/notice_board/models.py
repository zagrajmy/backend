from django.db import models

from crowd.models import User


class Guild(models.Model):
    """Small group of users or room during a convention."""

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, through="GuildUser")
    description = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # noqa D106
        db_table = "nb_guild"


class GuildUser(models.Model):
    """Membership model for guilds."""

    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=31)

    class Meta:  # noqa D106
        db_table = "nb_guild_user"


class Sphere(models.Model):
    """Big group for whole provinces, topics, organizations or big events."""

    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    class Meta:  # noqa D106
        db_table = "nb_sphere"


class Meeting(models.Model):
    """Meeting model."""

    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    sphere = models.ForeignKey("Sphere", on_delete=models.CASCADE)
    guild = models.ForeignKey("Guild", on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_time = models.DateTimeField(null=True)
    users = models.ManyToManyField(User, through="MeetingUser", related_name="meetings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.TextField(blank=True, null=True)

    class Meta:  # noqa D106
        db_table = "nb_meeting"


class MeetingUser(models.Model):
    """Meeting participation model."""

    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=31)

    class Meta:  # noqa D106
        db_table = "nb_meeting_user"
