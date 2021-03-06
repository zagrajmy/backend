# Generated by Django 3.1 on 2020-08-29 18:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notice_board", "0016_participants_limit"),
    ]

    operations = [
        migrations.CreateModel(
            name="MeetingParticipant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("CONFIRMED", "Confirmed"), ("WAITING", "Waiting")],
                        max_length=15,
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
                (
                    "meeting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notice_board.meeting",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "nb_meeting_participant",
                "unique_together": {("meeting", "user")},
            },
        ),
        migrations.AddField(
            model_name="meeting",
            name="participants",
            field=models.ManyToManyField(
                related_name="participated_meetings",
                through="notice_board.MeetingParticipant",
                to=settings.AUTH_USER_MODEL,
                verbose_name="participants",
            ),
        ),
    ]
