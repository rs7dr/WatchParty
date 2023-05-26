# Generated by Django 4.0.2 on 2022-05-03 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0047_alter_event_event_date_alter_event_event_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-05-02', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='20:02', null=True, verbose_name='Event Time'),
        ),
    ]