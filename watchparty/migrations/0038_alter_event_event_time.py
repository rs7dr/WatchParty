# Generated by Django 4.0.2 on 2022-04-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0037_alter_event_event_date_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='18:53', null=True, verbose_name='Event Time'),
        ),
    ]