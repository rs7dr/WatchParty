import datetime
from xmlrpc.client import DateTime
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CharField, Model

# title, image, similars, description, id, owner, similars
class Movie(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    similars = models.TextField(default="")
    title = models.TextField(default="")
    image = models.TextField(default="")
    year = models.TextField(default="")
    plot = models.TextField(default="")
    movie_id = models.TextField(default="")
    def __str__(self):
        return self.title

class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hometown = models.TextField(default="")
    title = models.TextField(default="")
    favorite_movies = models.TextField(default="")
    #number_of_events = models.TextField(default="0")  # Display later & connect to events, when they're working
    #number_of_events = models.IntegerField(default="0")?
    friends = models.ManyToManyField(User, related_name="Friends", default=0)
    #No longer need number_of_friends to be stored in the model, calculated in template
    description = models.TextField(default="")
    def __str__(self):
        return self.user.username

class Event(models.Model):
    # Many to many relationship for RSVP:
    # https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_many/
    # https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django#:~:text=When%20you%20design%20a%20database,solved%20using%20a%20ForeignKey%20alone.
    # https://stackoverflow.com/questions/17599035/django-how-can-i-call-a-view-function-from-template/19761466#19761466
    event_name = models.CharField('Event Name', default="", max_length=100, unique=False)
    event_date = models.DateTimeField('Event Date', blank=True, null=True, default = datetime.datetime.now().strftime('%Y-%m-%d'))
    event_time = models.TimeField('Event Time', blank=True, null=True, default = datetime.datetime.now().strftime('%H:%M'))
    event_type_choices = [('In-Person', 'In-Person'), ('Virtual', 'Virtual')] #Got rid of the old version, do not need separate function
    event_type = models.CharField('Event Type', choices=event_type_choices, max_length=100)
    event_location = models.CharField('Event Location', default="", max_length=100)
    event_description = models.TextField('Event Description', default="", max_length=400)
    event_owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL) #MyUser or User? SET_NULL or CASCADE?
    event_RSVP = models.ManyToManyField(User, related_name="RSVP", default=1)
    event_post_date = models.DateTimeField('Post Date', default=timezone.now)
    event_edit_date = models.DateTimeField('Edit Date', auto_now=True, blank=True, null=True) #Must call Model.save() somewhere in view if using this feature
    event_capacity = models.IntegerField(default=25)
    def __str__(self):
        return self.event_name
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.event_post_date <= now
    def get_absolute_url(self):
        return reverse("watchparty:listEvents")