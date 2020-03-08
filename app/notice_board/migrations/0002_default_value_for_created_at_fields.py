from django.db import migrations


def add_default_datetimes(apps, schema_editor):
    if schema_editor.connection.vendor.startswith('postgres'):
        schema_editor.execute('ALTER TABLE nb_guild ALTER COLUMN created_at SET DEFAULT now();')
        schema_editor.execute('ALTER TABLE nb_meeting ALTER COLUMN created_at SET DEFAULT now();')


def remove_default_datetimes(apps, schema_editor):
    if schema_editor.connection.vendor.startswith('postgres'):
        schema_editor.execute('ALTER TABLE nb_guild ALTER COLUMN created_at DROP DEFAULT;')
        schema_editor.execute('ALTER TABLE nb_meeting ALTER COLUMN created_at DROP DEFAULT;')


class Migration(migrations.Migration):

    dependencies = [
        ('notice_board', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_default_datetimes, remove_default_datetimes)
    ]
