# Generated by Django 4.0.2 on 2022-03-26 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('watchparty', '0002_myuser_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='myuser',
            name='number_of_events',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='number_of_friends',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Event Name')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('location', models.CharField(max_length=150, verbose_name='Event Location')),
                ('description', models.TextField(blank=True)),
                ('event_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]