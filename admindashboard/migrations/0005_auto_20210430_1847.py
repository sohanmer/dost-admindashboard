# Generated by Django 3.1.7 on 2021-04-30 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0004_merge_20210430_1843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programmodule',
            old_name='module_id',
            new_name='module',
        ),
        migrations.RenameField(
            model_name='programmodule',
            old_name='program_id',
            new_name='program',
        ),
    ]
