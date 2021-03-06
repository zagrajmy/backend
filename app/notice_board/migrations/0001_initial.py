# Generated by Django 2.2.10 on 2020-02-18 19:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'nb_guild',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('publication_time', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice_board.Guild')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nb_meeting',
            },
        ),
        migrations.CreateModel(
            name='Sphere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nb_sphere',
            },
        ),
        migrations.CreateModel(
            name='MeetingUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=31)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice_board.Meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nb_meeting_user',
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='sphere',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice_board.Sphere'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='users',
            field=models.ManyToManyField(related_name='meetings', through='notice_board.MeetingUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GuildUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(max_length=31)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notice_board.Guild')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'nb_guild_user',
            },
        ),
        migrations.AddField(
            model_name='guild',
            name='members',
            field=models.ManyToManyField(through='notice_board.GuildUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
