# Generated by Django 4.0.2 on 2022-04-25 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0042_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='20:28', null=True, verbose_name='Event Time'),
        ),
    ]
