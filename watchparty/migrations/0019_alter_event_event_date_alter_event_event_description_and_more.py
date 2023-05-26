# Generated by Django 4.0.2 on 2022-04-10 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0018_event_event_rsvp_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-04-09', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_description',
            field=models.TextField(default='', verbose_name='Event Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_location',
            field=models.CharField(default='', max_length=100, verbose_name='Event Location'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_name',
            field=models.CharField(default='', max_length=100, verbose_name='Event Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='21:10', null=True, verbose_name='Event Time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('In-Person', 'In-Person'), ('Virtual', 'Virtual')], max_length=100, verbose_name='Event Type'),
        ),
    ]