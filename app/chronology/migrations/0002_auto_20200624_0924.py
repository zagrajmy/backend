# Generated by Django 3.0.7 on 2020-06-24 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice_board', '0003_auto_20200601_2151'),
        ('chronology', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TimeTable',
            new_name='AgendaItem',
        ),
    ]
