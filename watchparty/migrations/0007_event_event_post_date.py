# Generated by Django 4.0.2 on 2022-03-27 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0006_event_event_time_event_event_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_post_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Post Date'),
        ),
    ]
