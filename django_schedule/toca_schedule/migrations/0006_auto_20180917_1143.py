# Generated by Django 2.1.1 on 2018-09-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toca_schedule', '0005_auto_20180917_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='action_id',
            field=models.CharField(max_length=100),
        ),
    ]
