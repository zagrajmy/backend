from django.db import models
from notice_board.models import Meeting, Sphere
from crowd.models import User

from django.contrib.postgres.fields import JSONField


class Festival(models.Model):
    end_time = models.DateTimeField()
    name = models.CharField(max_length=255)
    settings = JSONField(null=True)
    slug = models.SlugField(blank=True)
    sphere = models.ForeignKey(Sphere, on_delete=models.CASCADE)
    start_proposal = models.DateTimeField()
    start_publication = models.DateTimeField()
    start_time = models.DateTimeField()

    class Meta:
        db_table = "ch_festival"

    def __str__(self) -> None:
        return self.name


class Room(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "ch_room"

    def __str__(self) -> None:
        return self.name


class TimeSlot(models.Model):
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()

    class Meta:
        db_table = "ch_time_slot"

    def __str__(self) -> None:
        return f"From {self.start_time} to {self.end_time}"


class Helper(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    time_slots = models.ManyToManyField(TimeSlot)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "ch_helper"

    def __str__(self) -> None:
        return str(self.user)


class TimeTable(models.Model):
    end_time = models.DateTimeField()
    helper = models.ForeignKey(Helper, on_delete=models.SET_NULL, null=True)
    helper_confirmed = models.BooleanField(default=False)
    meeting = models.OneToOneField(Meeting, on_delete=models.SET_NULL, null=True)
    meeting_confirmed = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    start_time = models.DateTimeField()

    class Meta:
        db_table = "ch_time_table"


class WaitList(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "ch_wait_list"

    def __str__(self) -> None:
        return self.name


class Proposal(models.Model):
    city = models.CharField(max_length=255)
    club = models.CharField(max_length=255)
    description = models.TextField()
    needs = models.TextField()
    other_contact = models.TextField()
    other_data = models.TextField()
    phone = models.CharField(max_length=255)
    time_slots = models.ManyToManyField(TimeSlot)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waitlist = models.ForeignKey(WaitList, on_delete=models.CASCADE)

    class Meta:
        db_table = "ch_proposal"

    def __str__(self) -> None:
        return self.title
