# Generated by Django 3.0.7 on 2020-06-26 07:12
from django.db import migrations

import chronology.models
import common.json_field


class Migration(migrations.Migration):

    dependencies = [
        ('chronology', '0003_auto_20200624_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='festival',
            name='settings',
            field=common.json_field.JSONField(default=chronology.models.default_festival_settings),
        ),
    ]
