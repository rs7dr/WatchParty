# Generated by Django 4.0.2 on 2022-05-03 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0049_alter_event_event_time_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-05-03', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.TextField(default='', max_length=400, verbose_name='Event Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='12:14', null=True, verbose_name='Event Time'),
        ),
    ]
