
from __future__ import print_function
from httplib2 import Http
from Credentials import getCredentials
import datetime, logging
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def getUpcomingEvents(service, number_of_events, timeMin, calendarId='primary'):
    """
        Get upcoming events starting the current day.

            x Input :
                - number_of_events : number of events to get
                - timeMin : date for the beginning of the first event
                - calendarId : calendar you want to look up
            x Output : dict containing the events
    """
    logging.info("Getting the next %d upcoming events in your calendar ...")
    events_result = service.events().list(calendarId=calendarId, timeMin=timeMin,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime', showDeleted=True).execute()
    events = events_result.get('items', [])
    print(len(events), " events were found in : ", calendarId)
    for event in events:
        #print(event)
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    return events


def addEvent(service, event):
    """
        Adding an event to your calendar.
    """
    event = service.events().insert(calendarId='primary', body=event).execute()
    #logging.info('Event created: %s' % (event.get('htmlLink')))
    print('Event created: %s' % (event.get('htmlLink')))


def updateEventTitle(service, eventId, summary):#, NEW_EVENT):
    """
        Update the name of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['summary'] = summary
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    logging.info('Event updated: %s' % (event.get('htmlLink')))


def updateEventDate(service, eventId, startDate, endDate):
    """
        Update the date of an existing event.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    event['start']['dateTime'] = startDate
    event['end']['dateTime'] = endDate
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    logging.info('Event updated: %s' % (event.get('htmlLink')))

def addEventProperty(service, eventId, value, property, calendarId='primary'):
    """
        Add a property to an event.
    """
    event = service.events().get(calendarId=calendarId, eventId=eventId).execute()
    event[property] = value
    updated_event = service.events().update(calendarId=calendarId, eventId=event['id'], body=event).execute()
    logging.info(updated_event['updated'])

def deleteEvent(service, eventId):
    """
        Delete an event from your calendar.
    """
    event = service.events().get(calendarId='primary', eventId=eventId).execute()
    deleted_event = service.events().delete(calendarId='primary', eventId=event['id']).execute()
    logging.info('Event deleted: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    #CREDENTIAL_PATH = 'client_secret_163834025851-92js5g5aqpb8h8etbmukuu9uhv8t563u.apps.googleusercontent.com.json'
    creds = getCredentials() #insert your client_secret.json file path
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    getUpcomingEvents(service, 3, now, calendarId='primary')
    event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2020-12-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2020-12-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
    addEvent(service, event)
