# Generated by Django 4.0.2 on 2022-04-10 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchparty', '0025_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_RSVP',
            field=models.ManyToManyField(default=None, related_name='RSVP', to='watchparty.MyUser'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='17:37', null=True, verbose_name='Event Time'),
        ),
    ]