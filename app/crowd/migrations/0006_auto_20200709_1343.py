# Generated by Django 3.0.8 on 2020-07-09 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowd', '0005_add_sphere_admin_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth0_id',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
