from typing import Dict, TypedDict

from common.json_field import JSONField
from crowd.models import User
from django.db import models
from notice_board.models import Meeting, Sphere


class EmptyDict(TypedDict):
    pass


def default_festival_settings() -> Dict[str, EmptyDict]:
    return {"theme": {}, "forms": {}}


class Festival(models.Model):
    end_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    settings = JSONField(default=default_festival_settings)
    slug = models.SlugField(blank=True)
    sphere = models.ForeignKey(Sphere, on_delete=models.CASCADE)
    start_proposal = models.DateTimeField()
    start_publication = models.DateTimeField()
    start_time = models.DateTimeField()

    class Meta:
        db_table = "ch_festival"

    def __str__(self) -> str:
        return self.name


class Room(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "ch_room"

    def __str__(self) -> str:
        return self.name


class TimeSlot(models.Model):
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()

    class Meta:
        db_table = "ch_time_slot"

    def __str__(self) -> str:
        return f"From {self.start_time} to {self.end_time}"


class Helper(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    time_slots = models.ManyToManyField(TimeSlot)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "ch_helper"

    def __str__(self) -> str:
        return str(self.user)


class AgendaItem(models.Model):
    helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, null=True)
    helper_confirmed = models.BooleanField(default=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.SET_NULL, null=True)
    meeting_confirmed = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "ch_time_table"


class WaitList(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "ch_wait_list"

    def __str__(self) -> str:
        return self.name


class Proposal(models.Model):
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    STATUS_CHOICES = (
        (CREATED, "Created"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    duration_minutes = models.PositiveIntegerField()
    city = models.CharField(max_length=255)
    club = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=CREATED,)
    meeting = models.OneToOneField(Meeting, on_delete=models.CASCADE, null=True)
    needs = models.TextField()
    other_contact = models.TextField()
    other_data = models.TextField()
    phone = models.CharField(max_length=255)
    time_slots = models.ManyToManyField(TimeSlot)
    waitlist = models.ForeignKey(WaitList, on_delete=models.CASCADE)
    speaker_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="proposals", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    speaker_name = models.CharField(max_length=255)

    class Meta:
        db_table = "ch_proposal"

    def __str__(self) -> str:
        return self.name
