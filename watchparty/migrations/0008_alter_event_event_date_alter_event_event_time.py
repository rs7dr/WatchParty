# Generated by Django 4.0.2 on 2022-03-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0007_alter_event_event_date_alter_event_event_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-03-29', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='14:37', null=True, verbose_name='Event Time'),
        ),
    ]
