# project name: watch-party-347118
# email: watch-party@watchparty-347118.iam.gserviceaccount.com
# OAuth2 Client ID: 111637947079585840423
# Calendar ID string: aqe650bkoiqp23ropbe88pl9gc@group.calendar.google.com
#
# Google Account hosting API:
# cs3240b18@gmail.com
# Password: mcburney
from __future__ import print_function
from google.oauth2 import service_account
import googleapiclient.discovery
import datetime
from .models import Event

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = './google-credentials.json'
CAL_ID = 'aqe650bkoiqp23ropbe88pl9gc@group.calendar.google.com'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

def get_events(num_events):
    # global service
    # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=num_events).execute()
    events = events_result.get('items', [])
    return events

# From the tutorial
def demo_calendar():
    print("RUNNING DEMO_CALENDAR()")
    # CREATE A NEW EVENT
    new_event = {
        'summary': "Ben Hammond Tech's Super Awesome Event",
        'location': 'Denver, CO USA',
        'description': 'https://benhammond.tech',
        'start': {
            'date': f"{datetime.date.today()}",
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': f"{datetime.date.today() + datetime.timedelta(days=3)}",
            'timeZone': 'America/New_York',
        },
    }
    service.events().insert(calendarId=CAL_ID, body=new_event).execute()
    print('Event created')

    # commented out everything below here to run get_events()
    # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # LOG THEM ALL OUT IN DEV TOOLS CONSOLE
    for e in events:

        print(e)

    ### uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
    #service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()  #Event.event_name).execute()


    return events


# WORKING ON THIS AS FUNCTIONAL CALENDAR

def test_calendar(event):
    print("RUNNING TEST_CALENDAR()")
    # CREATE A NEW EVENT
    add_event = {
        'name': event.event_name,
        'host': event.event_owner,
        'location': event.event_location,
        'description': event.event_description,

        ## Change the date/time stuff
        'start': {
            'date': f"{datetime.date.today()}",
            'timeZone': 'America/New_York',
        },
        'end': {
            'date': f"{datetime.date.today() + datetime.timedelta(days=3)}",
            'timeZone': 'America/New_York',
        },
    }
    service.events().insert(calendarId=CAL_ID, body=add_event).execute()
    print('Event created')

    # commented out everything below here to run get_events()
    # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])

    # LOG THEM ALL OUT IN DEV TOOLS CONSOLE
    for e in events:

        print(e)

    ### uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
    #service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()  #Event.event_name).execute()


    return events


