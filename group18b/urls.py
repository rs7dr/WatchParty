from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from watchparty import views

urlpatterns = [
    path('', include('watchparty.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/google/login/', views.LoginView.as_view(), name='login'),
    path('editBio/', views.validate, name='editBio'),
    path('myBio/<str:username>/', views.myBioView, name='myBio'),
    path('searchResults/', views.searchResults, name='searchResults'),
    path('listEvents/', views.ListEvent.as_view(), name='events'),
    path('listRSVP/', views.ListRSVP.as_view(), name='rsvps'),
    path('listEvents/filter/', views.eventFilter, name='eventFilter'),
    path('createEvent/', views.CreateEvent.as_view(), name='createEvent'),
    path('listEvents/myEvents/', views.myEvents.as_view(), name='myEvents'),
    path('listEvents/<str:event_id>/', views.EventDetail, name='eventDetail'), #make event_id a number instead of based on event_name! Erorrs can occur with duplicate event names in database
    path('listEvents/<str:event_id>/editEvent', views.validate2, name='editEvent'),
    path('demo/', views.exportCalendar, name='demo'),
    path('add_to_favorites', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites', views.remove_from_favorites, name='remove_from_favorites'),
    path('friendSuggestions', views.ListFriends, name='friends')
]