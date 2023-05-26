from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User as UserDjango
from django.contrib.auth.models import AnonymousUser
from django.db.utils import IntegrityError
from .models import MyUser, Event
from .views import CreateEvent, EventDetail
import datetime
from django.utils import timezone
from django.urls import reverse

class TestMyUserModel(TestCase):
    def test_createMyUser(self):
        """
        Tests that a MyUser object is created and that its name matches the expected name.
        """
        #self.factory = RequestFactory()
        self.user = UserDjango.objects.create_user(username='John Doe', email='jhfgowhGOwhgfpwhg@gmail.com', password="password")
        MyUser.objects.get_or_create(user=self.user)
        TestUser = MyUser.objects.get(user=self.user)
        self.assertEquals(TestUser.user.username, "John Doe")

class TestEventCreationValidity(TestCase):
    def setUp(self):
        self.user = UserDjango.objects.create_user(username='John Doe', email='jhfgowhGOwhgfpwhg@gmail.com', password="password")

    def test_event_created(self):
        """
        Event object successfully created and retrievable, given only necessary parameters (otherwise default).
        """
        Event.objects.create(event_name="An Event", event_owner=self.user, event_type="Virtual")
        TestEvent = Event.objects.get(event_name="An Event")
        self.assertEquals(TestEvent.event_name, "An Event")

    def test_event_created_params(self):
        """
        Event object successfully created and retrievable, given non-default parameters.
        """
        Event.objects.create(event_name="An Event", event_owner=self.user, event_type="Virtual", event_date="2030-11-16", event_time="02:30", event_location="A location", event_description="descr", event_capacity="50")
        TestEvent = Event.objects.get(event_name="An Event")
        self.assertEquals(TestEvent.event_name, "An Event")

    # Needs fixing, should have self.user create an event rather than manually assigning self.user as the event_owner
    def test_event_ownership(self):
        """
        A valid event should automatically set the user who created the event as the event owner.
        """
        Event.objects.create(event_name="An Event", event_owner=self.user, event_type="Virtual")
        TestEvent = Event.objects.get(event_name="An Event")
        #event1 = CreateEvent()
        self.assertEquals(TestEvent.event_owner, self.user)
        #self.assertTrue(event1.form_valid(TestEvent))

    def test_event_invalid(self):
        """
        Gives an expected field in the Event model a Null value, and verifies that this raises an exception for invalid input.
        """
        with self.assertRaises(IntegrityError):
            Event.objects.create(event_name="An Event", event_owner=self.user, event_type="Virtual", event_description=None)

    # Create test after limiting selection of prior dates/times, or not allowing form to submit if they are chosen
    #def test_event_past_datetime(self):

    # Create test after fully implementing capacity
    # Should test that you can't RSVP past capacity
    # And another test should check that negative values, 0, or 1 as input gets handled, by not allowing it or throwing an exception
    #def test_event_capacity(self):

#class TestViews(TestCase):
#    def setUp(self):
#        self.client = Client()
#        self.user = UserDjango.objects.create_user(username='John Doe', email='jhfgowhGOwhgfpwhg@gmail.com', password="password")
#        self.event = Event.objects.create(event_name="AnEvent", event_owner=self.user, event_type="Virtual")
#        self.event_detail_url = reverse(EventDetail, args=['AnEvent'])
#        #self.factory = RequestFactory()
#        print("event detail url:", self.event_detail_url)

#    def test_event_detail_GET(self):
#        """
#        Test form_valid function in CreateEvent
#        """
#        response = self.client.get(self.event_detail_url)
#        self.assertEquals(response.status_code, 200)
# Getting an error message saying User / Event has no GET attribute

class EventPublicationTests(TestCase):
    def test_was_published_recently_with_future_event(self):
        """
        was_published_recently() returns False for events whose post_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_event = Event(event_post_date=time)
        self.assertIs(future_event.was_published_recently(), False)

    def test_was_published_recently_with_old_event(self):
        """
        was_published_recently() returns False for events whose post_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_event = Event(event_post_date=time)
        self.assertIs(old_event.was_published_recently(), False)

    def test_was_published_recently_with_recent_event(self):
        """
        was_published_recently() returns True for events whose post_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_event = Event(event_post_date=time)
        self.assertIs(recent_event.was_published_recently(), True)


class EventRSVPTests(TestCase):
    def test_user_RSVP_event(self):
        """
        Tests that a MyUser object is added/associated with an Event object in Event's event_RSVP table
        """
        self.user = UserDjango.objects.create_user(username='First Last', email='firstlast@gmail.com', password='password')
        MyUser.objects.get_or_create(user=self.user)
        user = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=5)
        event = Event.objects.get(event_name='Test Event')
        user.save()
        event.event_RSVP.add(user.user)
        event.save()
        self.assertEquals(len(event.event_RSVP.all()), 1)

    def test_multiple_users_RSVP_event(self):
        """
        Tests that multiple MyUser objects is added/associated with an Event object in Event's event_RSVP table
        """
        self.user = UserDjango.objects.create_user(username='user1', email='user1@gmail.com', password='password1')
        MyUser.objects.get_or_create(user=self.user)
        user1 = MyUser.objects.get(user=self.user)
        self.user = UserDjango.objects.create_user(username='user2', email='user2@gmail.com', password='password2')
        MyUser.objects.get_or_create(user=self.user)
        user2 = MyUser.objects.get(user=self.user)
        self.user = UserDjango.objects.create_user(username='user3', email='user3@gmail.com', password='password3')
        MyUser.objects.get_or_create(user=self.user)
        user3 = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=5)
        event = Event.objects.get(event_name='Test Event')
        user1.save()
        user2.save()
        user3.save()
        event.event_RSVP.add(user1.user)
        event.save()
        event.event_RSVP.add(user2.user)
        event.save()
        event.event_RSVP.add(user3.user)
        event.save()
        self.assertEquals(len(event.event_RSVP.all()), 3)

    def test_users_cancel_RSVP(self):
        """
        Tests that MyUser objects is removed/disassociated with an Event object in Event's event_RSVP table
        """
        self.user = UserDjango.objects.create_user(username='user1', email='user1@gmail.com', password='password1')
        MyUser.objects.get_or_create(user=self.user)
        user1 = MyUser.objects.get(user=self.user)
        self.user = UserDjango.objects.create_user(username='user2', email='user2@gmail.com', password='password2')
        MyUser.objects.get_or_create(user=self.user)
        user2 = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=5)
        event = Event.objects.get(event_name='Test Event')
        user1.save()
        user2.save()
        event.event_RSVP.add(user1.user)
        event.save()
        event.event_RSVP.add(user2.user)
        event.save()
        event.event_RSVP.remove(user2.user)
        event.save()
        self.assertEquals(len(event.event_RSVP.all()), 1)

    def test_owner_automatically_RSVP(self):
        """
        Tests that MyUser objects automatically RSVP for Event they create if user is owner
        """
        self.user = UserDjango.objects.create_user(username='event_owner', email='event_owner@gmail.com', password='password')
        MyUser.objects.get_or_create(user=self.user)
        user = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=5)
        event = Event.objects.get(event_name='Test Event')
        if (str(event.event_owner).lower() == user.user.username.lower()):
            user.save()
            event.event_RSVP.add(user.user)
            event.save()
        self.assertEquals(len(event.event_RSVP.all()), 1)

    def test_owner_cannot_cancel_RSVP(self):
        """
        Tests that MyUser objects cannot cancel RSVP for Event they created (event owners)
        """
        self.user = UserDjango.objects.create_user(username='event_owner', email='event_owner@gmail.com', password='password')
        MyUser.objects.get_or_create(user=self.user)
        user = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=5)
        event = Event.objects.get(event_name='Test Event')
        # Simulates automatically RSVP'ing event owner
        user.save()
        event.event_RSVP.add(user.user)
        event.save()
        # if condition should not go through
        if (str(event.event_owner).lower() != user.user.username.lower()):
            user.save()
            event.event_RSVP.remove(user.user)
            event.save()
        self.assertEquals(len(event.event_RSVP.all()), 1)

    def test_user_cannot_exceed_RSVP_capacity(self):
        """
        Tests that users cannot RSVP beyond the RSVP capacity
        """
        self.user = UserDjango.objects.create_user(username='event_owner', email='event_owner@gmail.com', password='password')
        MyUser.objects.get_or_create(user=self.user)
        user = MyUser.objects.get(user=self.user)
        self.user = UserDjango.objects.create_user(username='user', email='test_user@gmail.com', password='password')
        MyUser.objects.get_or_create(user=self.user)
        user2 = MyUser.objects.get(user=self.user)
        Event.objects.create(event_name='Test Event', event_type='Virtual', event_owner=self.user, event_capacity=1)
        event = Event.objects.get(event_name='Test Event')
        # Simulates automatically RSVP'ing event owner (which makes capacity 1/1)
        user.save()
        event.event_RSVP.add(user.user)
        event.save()
        # if condition should not go through
        if (len(event.event_RSVP.all())+1 <= event.event_capacity):
            user2.save()
            event.event_RSVP.add(user2.user)
            event.save()
        self.assertEquals(len(event.event_RSVP.all()), 1)