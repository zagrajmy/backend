from datetime import datetime
from typing import Optional

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from crowd.models import User

from .models import Guild, Meeting, Sphere


class MeetingCreateSerializer(serializers.ModelSerializer):
    guild = serializers.PrimaryKeyRelatedField(many=False, queryset=Guild.objects)
    organizer = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects)
    sphere = serializers.PrimaryKeyRelatedField(many=False, queryset=Sphere.objects)

    class Meta:
        model = Meeting
        exclude = ["created_at", "image", "participants", "status", "updated_at"]

    def validate_guild(self, guild: Optional[Guild]) -> Optional[Guild]:
        if (
            guild
            and not guild.members.filter(
                uuid=self.context["request"].user.uuid
            ).exists()
        ):
            raise serializers.ValidationError(
                _("You cannot add a meeting to a guild you don't belong!")
            )
        return guild

    def validate_organizer(self, organizer: Optional[User]) -> Optional[User]:
        if organizer != self.context["request"].user:
            raise serializers.ValidationError(
                _("You cannot add a meeting as a different person!")
            )
        return organizer

    @staticmethod
    def validate_start_time(start_time: Optional[datetime]) -> Optional[datetime]:
        if start_time and start_time < timezone.now():
            raise serializers.ValidationError(
                _("You cannot add a meeting in the past!")
            )
        return start_time


class MeetingReadSerializer(serializers.ModelSerializer):
    guild = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    organizer = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sphere = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        fields = "__all__"
        model = Meeting


class MeetingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        exclude = [
            "created_at",
            "guild",
            "image",
            "organizer",
            "participants",
            "sphere",
            "status",
            "updated_at",
        ]

    def _validate_time_value(
        self, field: str, value: Optional[datetime]
    ) -> Optional[datetime]:
        if (
            value
            and self.instance
            and getattr(self.instance, field) != value
            and self.instance.status == "past"
        ):
            raise serializers.ValidationError(
                _("You cannot change the time of a past event!")
            )
        return value

    def validate_end_time(self, end_time: Optional[datetime]) -> Optional[datetime]:
        return self._validate_time_value("end_time", end_time)

    def validate_publication_time(
        self,
        publication_time: Optional[datetime],
    ) -> Optional[datetime]:
        return self._validate_time_value("publication_time", publication_time)

    def validate_start_time(self, start_time: Optional[datetime]) -> Optional[datetime]:
        return self._validate_time_value("start_time", start_time)
