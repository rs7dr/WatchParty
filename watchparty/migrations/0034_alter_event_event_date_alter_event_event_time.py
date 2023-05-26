# Generated by Django 4.0.2 on 2022-04-17 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0033_alter_event_event_date_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-04-17', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='15:21', null=True, verbose_name='Event Time'),
        ),
    ]
