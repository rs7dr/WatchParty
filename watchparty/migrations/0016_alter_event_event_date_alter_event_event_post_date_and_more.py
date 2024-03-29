# Generated by Django 4.0.2 on 2022-04-08 17:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0015_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default='2022-04-08', null=True, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_post_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Post Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='13:33', null=True, verbose_name='Event Time'),
        ),
    ]
