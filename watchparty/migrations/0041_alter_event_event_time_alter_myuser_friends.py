# Generated by Django 4.0.2 on 2022-04-24 23:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchparty', '0040_remove_myuser_number_of_friends_myuser_friends_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='19:08', null=True, verbose_name='Event Time'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='friends',
            field=models.ManyToManyField(default=0, related_name='Friends', to=settings.AUTH_USER_MODEL),
        ),
    ]
