# Generated by Django 3.0.8 on 2020-07-04 13:29

from django.db import migrations

import chronology.models
import common.json_field


class Migration(migrations.Migration):

    dependencies = [
        ("chronology", "0007_add_timeslot_festival_fk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="proposal",
            name="other_contact",
            field=common.json_field.PostgreSQLJSONField(
                default=chronology.models.default_json_field, null=True
            ),
        ),
        migrations.AlterField(
            model_name="proposal",
            name="other_data",
            field=common.json_field.PostgreSQLJSONField(
                default=chronology.models.default_json_field, null=True
            ),
        ),
        migrations.AlterModelTable(name="agendaitem", table="ch_agenda_item",),
    ]
