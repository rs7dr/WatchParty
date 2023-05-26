from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyUser, Event, Movie
from .calendar_API import *
from django.utils.timezone import make_aware
from datetime import datetime
import datetime

# IMDB API Key: k_iurhxzst
class IndexView(generic.ListView):
    template_name = 'watchparty/index.html'
    context_object_name = 'recent_events'

    def get_queryset(self):
        """Return the next three events from current day"""
        """anything outside of a week isn't considered"""
        target = datetime.date.today() + datetime.timedelta(days=7)
        return Event.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date', 'event_time')[:3]

class LogoutView(generic.ListView):
    template_name = 'watchparty/logout.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return 1

class LoginView(generic.ListView):
    template_name = 'socialaccount/logout.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return 1

class BioView(generic.ListView):
    template_name = 'socialaccount/editBio.html'
    def bio_view(request):
        return render(request, "editBio.html")  # return response
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return 1

class CreateEvent(LoginRequiredMixin, generic.CreateView): #user must be logged in to create event so event automatically identifies with user
    model = Event
    fields = ['event_name',  'event_date', 'event_time', 'event_type', 'event_capacity', 'event_location', 'event_description'] #no longer need "event_owner" as a field due to form validation function
    template_name = 'socialaccount/createEvent.html'
    def get_success_url(self):
        return reverse('events')
    #In order to correctly track who created the event automatically: https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        listOfEventNames = [e.event_name for e in Event.objects.filter(event_date__gte=datetime.date.today())]
        if form.instance.event_name in listOfEventNames:
            message = "That event name is already taken, please choose another."
            return render(self.request, "socialaccount/error.html", {'message': message})
        elif (form.instance.event_capacity < 2):
            message = "Please choose a capacity greater than 1 attendee."
            return render(self.request, "socialaccount/error.html", {'message': message})
        elif (form.instance.event_capacity > 10000):
            message = "Wow that's a big event...please choose a capacity of less than 10,000 people."
            return render(self.request, "socialaccount/error.html", {'message': message})
        elif form.instance.event_date is None:
            message = "Please select a date for your event."
            return render(self.request, "socialaccount/error.html", {'message': message})
        elif form.instance.event_date.date() < datetime.date.today():
            message = "Please choose an event date that is not in the past."
            return render(self.request, "socialaccount/error.html", {'message': message})
        elif form.instance.event_time is None:
            message = "Please select a starting time for your event."
            return render(self.request, "socialaccount/error.html", {'message': message})
        else:
            form.instance.event_owner = self.request.user
            form.save()
            form.instance.event_RSVP.add(self.request.user) #automatically RSVP event owner after posting event
            return super().form_valid(form) #automatically calls form.save() for ManyToMany association
    # def form_invalid(self, form):
    #     listOfEventNames = [e.event_name for e in Event.objects.filter(event_date__gte=datetime.date.today())]
    #     if form.instance.event_name in listOfEventNames:
    #         message = "That event name is already taken, please choose another."
    #         return render(self.request, "socialaccount/error.html", {'message': message})
    #         #form.add_error('event_name', 'event name is lready in use')
    #         #return render(self.request, 'socialaccount/createEvent.html', {'form': form, 'event_name': form.instance.event_name, 'event_cap': form.instance.event_capacity})
    #     elif (form.instance.event_capacity < 2):
    #         message = "Please choose a capacity greater than 2 attendees"
    #         return render(self.request, "socialaccount/error.html", {'message': message})
        
    #     elif form.instance.event_date.date() < datetime.date.today():
    #         message = "Please choose an event date that is not in the past"
    #         return render(self.request, "socialaccount/error.html", {'message': message})
    #     else:
    #         return super().form_valid(form)

class ListEvent(generic.ListView):
    model = Event
    template_name = 'watchparty/listEvents.html'
    context_object_name = 'events_list'
    def get_queryset(self):
        return Event.objects.all().filter(event_date__gte=datetime.date.today()).order_by('event_date', 'event_time')

class myEvents(generic.ListView):
    model = Event
    template_name = 'watchparty/myEvents.html'
    context_object_name = 'my_events'
    def get_queryset(self):
        user = User.objects.get(username=self.request.user.username)
        return Event.objects.all().filter(event_owner=user).order_by('event_date', 'event_time')

class ListRSVP(generic.ListView):
    model = Event
    template_name = 'watchparty/listRSVP.html'
    context_object_name = 'events_RSVP_list'
    def get_queryset(self):
        user = User.objects.get(username=self.request.user.username)
        return user.RSVP.all().filter(event_date__gte=datetime.date.today()).order_by('event_date', 'event_time')

# validates edit bio
def validate(request):
    # Pull the user from the Database
    user = request.user
    MyUser.objects.get_or_create(user=user)
    name = user.username
    hometown = user.myuser.hometown
    favorite_movies = user.myuser.favorite_movies
    title = user.myuser.title
    description = user.myuser.description
    # Check if any values are missing
    if user.username == None: 
        name = ""
    if user.myuser.hometown == None:
        hometown = ""
    if user.myuser.title == None:
        title = ""
    if user.myuser.description == None:
        description = ""
    # When form is submitted, update in database and also update the user
    if request.method == "POST":
        name = request.POST["your_name"]
        hometown = request.POST["hometown"]
        title = request.POST["title"]
        description = request.POST["description"]
        user.myuser.hometown = hometown
        user.myuser.description = description
        user.myuser.favorite_movies = favorite_movies
        user.myuser.title = title
        user.myuser.save()
        usernames = [name.username for name in User.objects.all()]
        if name == user.username:
            user.username = name
            user.save()
            s = '/myBio' + '/' + user.username
            return redirect(s, {'user': user, "requester": user})
        elif name != user.username and name not in usernames:
            user.username = name
            user.save()
            s = '/myBio' + '/' + user.username
            return redirect(s, {'user': user, "requester": user})
        else:
            message = "That username is already taken, please choose another one."
            return render(request, "socialaccount/error.html", {'message': message})
        #return render(request, "socialaccount/myBio.html", {'user': user})  # out of reach
    return render(request, "socialaccount/editBio.html", {'name': name, 'hometown':hometown, 'description': description, 'title': title, 'favorite_movies':favorite_movies})

# validates edit event
def validate2(request, event_id):
    # Pull the user from Database
    user = request.user
    event = Event.objects.get_or_create(event_owner=user, event_name=request.path.split("/")[2])
    event = event[0]
    initial_event_name = event.event_name
    event_date = event.event_date
    event_time = event.event_time
    event_type_choices = event.event_type_choices
    event_type = event.event_type
    event_location = event.event_location
    event_description = event.event_description
    event_owner = event.event_owner
    event_RSVP = event.event_RSVP
    event_post_date = event.event_post_date
    event_edit_date = event.event_edit_date
    event_capacity = event.event_capacity

    if request.method == "POST":
        event_name = request.POST["event_name"]
        event_capacity = request.POST["event_capacity"]
        event_date = request.POST["event_date"]
        event_time = request.POST["event_time"]
        event_type = request.POST["event_type"]
        event_location = request.POST["event_location"]
        event_description = request.POST["event_description"]
        event.event_name = event_name
        event.event_capacity = event_capacity
        event.event_date = event_date
        event.event_time = event_time
        event.event_type = event_type
        event.event_location = event_location
        event.event_description = event_description
        listOfEventNames = [e.event_name for e in Event.objects.filter(event_date__gte=datetime.date.today())]
        if event_name in listOfEventNames and event_name != initial_event_name:
            message = "That event name is already taken, please choose another one."
            return render(request, "socialaccount/error.html", {'message': message})
        elif int(event_capacity) < 2:
            message = "Please choose a capacity greater than 1 attendee."
            return render(request, "socialaccount/error.html", {'message': message})
        elif int(event_capacity) > 10000:
            message = "Wow that's a big event...please choose a capacity of less than 10,000 people."
            return render(request, "socialaccount/error.html", {'message': message})
        elif event_date is None:
            message = "Please select a date for your event."
            return render(request, "socialaccount/error.html", {'message': message})
        elif datetime.datetime.strptime(event_date, "%Y-%m-%d").date() < datetime.date.today():
            message = "Please choose an event date that is not in the past."
            return render(request, "socialaccount/error.html", {'message': message})
        elif event_time is None:
            message = "Please select a starting time for your event."
            return render(request, "socialaccount/error.html", {'message': message})
        else:
            event.save()
            s = '/listEvents' + '/' + event.event_name
            return redirect(s, {'event': event, 'user': user})
    return render(request, "watchparty/editEvent.html", {'event_name': event, 'event_capacity': event_capacity,
        'event_date': event_date.strftime("%Y-%m-%d"), 'event_time': event_time.strftime("%H:%M"),
        'event_type': event_type, 'event_location': event_location, "event_description": event_description})

def myBioView(request, username):
    #Render the movie list
    requester = request.user
    user = User.objects.get(username=username)
    movies = Movie.objects.filter(owner=user)
    # title, image, similars, year, plot, id, owner, similars
    titles = []
    images = []
    years = []
    plots = []
    movie_ids = []

    for movie in movies: 
        titles.append(movie.title)
        images.append(movie.image)
        years.append(movie.year)
        plots.append(movie.plot)
        movie_ids.append(movie.movie_id)

    movie_titles = ""
    for title in titles:
        if movie_titles == "":
            movie_titles = title
        else:
            movie_titles = movie_titles + ", " + title

    MyUser.objects.get_or_create(user=user)
    # # If you are visting a different person's page
    # if request.user.username != username:
    #     favorite_movies = user.myuser.favorite_movies
    # else:
    #     favorite_movies = requester.myuser.favorite_movies 
    # movies_list = favorite_movies.split(" ")
    # movie_jsons = []
    # titles = []
    # types = []
    # years = []
    # images = []
    # runtime = []
    # directors = []
    # stars = []
    # ids = []

    # for movie in movies_list:
    #     movie_info = requests.get('https://imdb-api.com/en/API/Title/k_iurhxzst/'+movie)
    #     json_dictionary = movie_info.json()
    #     movie_jsons.append(json_dictionary)

    #     if (json_dictionary['title'] != None):
    #         titles.append(json_dictionary['title'])
    #         types.append(json_dictionary['type'])
    #         years.append(json_dictionary['year'])
    #         images.append(json_dictionary['image'])
    #         runtime.append(json_dictionary['runtimeStr'])
    #         directors.append(json_dictionary['directors'])
    #         stars.append(json_dictionary['stars'])
    #         ids.append(json_dictionary['id'])
    
    # If visitor of Bio
    if request.user.username != username:
        user = User.objects.get(username=username)
        editBio = False
        alreadyFriends = False
        # Set up two-way friends list
        friends_list = []
        for friended_you in user.myuser.friends.all():
            friends_list.append(friended_you)
        for you_friended in user.Friends.all():
            if you_friended.user not in user.myuser.friends.all():
                friends_list.append(you_friended.user)
        for friend in friends_list:
            if request.user.username == friend.username:
                alreadyFriends = True
                break
        if (request.GET.get('Remove_Friend_Button')):
            user.myuser.friends.remove(request.user) # apparently you need BOTH of these...but only 1 for add???
            user.Friends.remove(request.user.myuser) # apparently you need BOTH of these...but only 1 for add???
            user.save()
            alreadyFriends = False
            # Reset two-way friends list after removing friend
            friends_list = []
            for friended_you in user.myuser.friends.all():
                friends_list.append(friended_you)
            for you_friended in user.Friends.all():
                if you_friended.user not in user.myuser.friends.all():
                    friends_list.append(you_friended.user)
            return render(request, "socialaccount/myBio.html", {'results': zip(titles, images, years, plots, movie_ids), 'movie_titles':movie_titles,'user': user, 'editBio': editBio, "friend_status": alreadyFriends, "friends_list": friends_list, "requester": requester})
        if (request.GET.get('Friend_Button')):
            user.myuser.friends.add(request.user)
            user.save()
            alreadyFriends = True
            # Reset two-way friends list after adding friend
            friends_list = []
            for friended_you in user.myuser.friends.all():
                friends_list.append(friended_you)
            for you_friended in user.Friends.all():
                if you_friended.user not in user.myuser.friends.all():
                    friends_list.append(you_friended.user)
            return render(request, "socialaccount/myBio.html", {'results': zip(titles, images, years, plots, movie_ids), 'movie_titles':movie_titles,'user': user, 'editBio': editBio, "friend_status": alreadyFriends, "friends_list": friends_list, "requester": requester})
        return render(request, "socialaccount/myBio.html", {'results': zip(titles, images, years, plots, movie_ids), 'movie_titles':movie_titles,'user': user, 'editBio': editBio, "friend_status": alreadyFriends, "friends_list": friends_list, "requester": requester})
    # If owner of Bio
    else:
        user = request.user
        editBio = True
        # Set up two-way friends list
        friends_list = []
        for friended_you in user.myuser.friends.all():
            friends_list.append(friended_you)
        for you_friended in user.Friends.all():
            if you_friended.user not in user.myuser.friends.all():
                friends_list.append(you_friended.user)
        return render(request, "socialaccount/myBio.html", {'results': zip(titles, images, years, plots, movie_ids), 'movie_titles':movie_titles, 'user': user, 'editBio': editBio, "friends_list": friends_list, "requester": requester})

def EventDetail(request, event_id):
    event = Event.objects.get(event_name=event_id) # WARNING: must make primary key of an Event NOT event_name, something unique like ID
    user = request.user
    # Logic for checking if user is owner then automatically RSVP and display different buttons
    if (str(event.event_owner).lower() == user.username.lower()):
        # Logic for if owner clicks "Edit Event" button, must be owner
        if ((request.GET.get('Edit_Button')) and (str(event.event_owner).lower() == user.username.lower())):
            return redirect('editEvent', event.event_name)
        # Logic for if owner clicks "Export Event" button
        '''Here is Export Button'''
        if (request.GET.get('Export_Button')):
            return redirect('demo', permanent=True)
        # Logic for if owner clicks "Delete Event" button, must be owner and remove all RSVP
        if ((request.GET.get('Delete_Button')) and (str(event.event_owner).lower() == user.username.lower())):
            for name in event.event_RSVP.all():
                event.event_RSVP.remove(name)
            event.save()
            # WARNING: this is why event_name cannot be a primary key for event_id
            # must change later, users could create events with same name and Event.objects.get() will throw an error
            event.delete()
            return redirect('events', permanent=True)
    else:
        # Logic for if user clicks "RSVP Event" button, cannot be owner or exceed capacity
        if ((request.GET.get('RSVP_Button')) and (str(event.event_owner).lower() != user.username.lower()) and (len(event.event_RSVP.all())+1 <= event.event_capacity)):
            user.save()
            event.event_RSVP.add(user)
            event.save()
            return render(request, 'watchparty/eventDetail.html', {'event': event, 'user': user})
        # Logic for if owner clicks "Export Event" button
        if (request.GET.get('Export_Button')):
            return redirect('demo', permanent=True)
        # Logic for if user clicks "Cancel RSVP" button, cannot be owner or exceed capacity
        if ((request.GET.get('CancelRSVP_Button')) and (str(event.event_owner).lower() != user.username.lower()) and (len(event.event_RSVP.all()) <= event.event_capacity)):
            user.save()
            event.event_RSVP.remove(user)
            event.save()
            return render(request, 'watchparty/eventDetail.html', {'event': event, 'user': user})
    return render(request, "watchparty/eventDetail.html", {'event': event, 'user': user})

def eventFilter(request):
    if (request.GET.get('Filter_Button')):
        return redirect('watchparty/filterEvent', permanent=True)

#def get_queryset(self):
        #"""Return all events owned by user """
        #"""anything outside of a week isn't considered"""
        #target = datetime.date.today() + datetime.timedelta(days=7)
        #return Event.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date', 'event_time')[:3]

# add event_id as a parameter and uncomment event = and test_calendar lines
def exportCalendar(request, event_id):
    #event = Event.objects.get(event_name=event_id)
    # Do stuff here:
    #results = get_events(5)  # will only show 5 events
    results = mac(event_id)  # the dummy event
    #results = test_calendar(event)  # our actual calendar, eventually
    context = {"results": results}
    return render(request, 'watchparty/demo.html', context)

def searchResults(request):
    searchName = request.GET.get('search')
    if request.method == "GET" and len(searchName) != 0:
        search_results = requests.get('https://imdb-api.com/en/API/SearchTitle/k_iurhxzst/'+searchName) 
        url = 'watchparty/searchResults.html'
        json_dictionary = search_results.json()
        results = json_dictionary['results']
        len_of_results = len(results)
        if (len_of_results > 10):
            len_of_results = 10

        titles = []
        images = []
        description = []
        IDs = []
        # for i in range(len_of_results):
        #     current_result = results['i']
        i = 0
        for result in results:
            if i > 10:
                break
            titles.append(result['title'])
            images.append(result['image'])
            description.append(result['description'])
            IDs.append(result['id'])
            i += 1
        return render(request, url, {'results': zip(titles, images, description, IDs), 'searchName': searchName})
    else:
        url = 'watchparty/index.html'
    return render(request, url, {})

def add_to_favorites(request):
    if request.method == "GET":
        # Get the user.
        user = request.user
        MyUser.objects.get_or_create(user=user)
        # Get the movie ID
        movie_id = request.GET.get('movie_id')
        # Make title API call to get more information about the movie 
        movie_info = requests.get('https://imdb-api.com/en/API/Title/k_iurhxzst/'+movie_id)
        json_dictionary = movie_info.json()

        if (json_dictionary['title'] != None):
            title = json_dictionary['title']
            image = json_dictionary['image']
            year = json_dictionary['year']
            plot = json_dictionary['plot']
            similars_dictionary = json_dictionary['similars']
            len_of_similars = len(similars_dictionary)
            if (len_of_similars > 10):
                len_of_similars = 10
            similars = ""
            i = 0
            for similar in similars_dictionary:
                if i > 10:
                    break
                if similars == "":
                    similars = similar['id']
                else:
                    similars = similars + " " + similar['id']
                i += 1
        # title, image, similars, year, plot, id, owner, similars
        movie = Movie.objects.get_or_create(
            owner=user,
            title=title,
            image=image,
            similars=similars,
            year=year,
            plot=plot,
            movie_id=movie_id
            )
        s = 'myBio' + '/' + user.username
        return redirect(s, {'movie':movie, 'user':user})

def remove_from_favorites(request):
    if request.method == "GET":
        user = request.user
        MyUser.objects.get_or_create(user=user)
        movie_id = request.GET.get('movie_id')

        movie = Movie.objects.filter(owner=user, movie_id = movie_id)

        movie.delete()


        # Get the movie that we want to delete

        user.myuser.save()
        s = 'myBio' + '/' + user.username
        return redirect(s, {'user':user})

def ListFriends(request):
    user = request.user
    movies = Movie.objects.all().filter(owner=user)
    similar_movies_string = ""
    for movie in movies:
        similar_movies_string += movie.similars
    similar_movies_array = similar_movies_string.split(" ")

    friend_recommendations = set()
    
    all_users = User.objects.all()
    for each_user in all_users:
        each_users_movies = Movie.objects.all().filter(owner=each_user)
        each_users_similar_movies_string = ""
        for user_movie in each_users_movies:
            each_users_similar_movies_string += user_movie.similars
        each_users_similar_movies_array = each_users_similar_movies_string.split(" ")
        for match in each_users_similar_movies_array:
            if ((match in similar_movies_array) and (each_user not in friend_recommendations) and (each_user.username!=user.username)):
                friend_recommendations.add(each_user.username)
    return render(request, "socialaccount/friendSuggestions.html", {'friend_suggestions': friend_recommendations, 'user': user})