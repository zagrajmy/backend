# Generated by Django 3.0.6 on 2020-06-01 19:51

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("notice_board", "0002_default_value_for_created_at_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="GuildMember",
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
                    "membership_type",
                    models.CharField(
                        choices=[
                            ("applied", "Applied"),
                            ("member", "Member"),
                            ("admin", "Admin"),
                        ],
                        max_length=255,
                    ),
                ),
            ],
            options={"db_table": "nb_guild_member",},
        ),
        migrations.RemoveField(model_name="meetinguser", name="meeting",),
        migrations.RemoveField(model_name="meetinguser", name="user",),
        migrations.RenameField(
            model_name="meeting", old_name="title", new_name="name",
        ),
        migrations.RemoveField(model_name="meeting", name="users",),
        migrations.RemoveField(model_name="sphere", name="users",),
        migrations.AddField(
            model_name="guild",
            name="is_public",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="guild", name="slug", field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name="guild",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="meeting", name="meeting_url", field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="participants",
            field=models.ManyToManyField(
                related_name="participated_meetings", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="meeting", name="slug", field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name="sphere",
            name="is_open",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="sphere",
            name="managers",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="sphere",
            name="settings",
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name="sphere",
            name="site",
            field=models.OneToOneField(
                null=True, on_delete=django.db.models.deletion.PROTECT, to="sites.Site"
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="organizer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="organized_meetings",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="guild",
            name="members",
            field=models.ManyToManyField(
                through="notice_board.GuildMember", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(name="GuildUser",),
        migrations.DeleteModel(name="MeetingUser",),
        migrations.AddField(
            model_name="guildmember",
            name="guild",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="notice_board.Guild"
            ),
        ),
        migrations.AddField(
            model_name="guildmember",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]