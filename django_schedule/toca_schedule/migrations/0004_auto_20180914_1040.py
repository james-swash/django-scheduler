# Generated by Django 2.1.1 on 2018-09-14 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toca_schedule', '0003_auto_20180912_1334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='description',
            new_name='action_id',
        ),
    ]
