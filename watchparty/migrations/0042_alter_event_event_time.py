# Generated by Django 4.0.2 on 2022-04-24 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0041_alter_event_event_time_alter_myuser_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='19:50', null=True, verbose_name='Event Time'),
        ),
    ]