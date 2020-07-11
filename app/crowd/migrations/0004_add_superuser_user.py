# Generated by Django 3.0.6 on 2020-05-15 08:04

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def add_superuser(apps, schema_editor):
    if settings.DEBUG:
        User = apps.get_model("crowd", "User")

        admin, __ = User.objects.get_or_create(username="admin",)

        admin.is_active = True
        admin.is_superuser = True
        admin.is_staff = True
        admin.password = make_password("proudweasel")
        admin.save()


def delete_superuser(apps, schema_editor):
    if settings.DEBUG:
        User = apps.get_model("crowd", "Group")

        User.objects.filter(username="admin").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("crowd", "0003_auto_20200617_0959"),
    ]

    operations = [migrations.RunPython(add_superuser, delete_superuser)]
