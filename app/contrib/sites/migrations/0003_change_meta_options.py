# Generated by Django 3.1 on 2020-08-11 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_update_default_site'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ['domain'], 'verbose_name': 'site', 'verbose_name_plural': 'sites'},
        ),
    ]
