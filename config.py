import datetime
import datefinder
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'credentials.json'

def get_calendar():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service


def u_input():
    '''Taking in user input for creating an event'''
 
    print("Adding an event ... ")
    summary = input("Event (ie 'code_clinic') : ")
    start_time = input("Date & Time (ie 25 Jul 13.30pm ) : ")
    desc = input("Topic of speciality : ")
    add_event(start_time, summary, desc)

    return summary, start_time, desc
    

def add_event(start_time, summary, desc):
   
   service = get_calendar()
   timer = list(datefinder.find_dates(start_time))

   if len(timer):
       start = timer[0]
       end = start + timedelta(minutes = 30)

   event_result = service.events().insert(calendarId='primary',
       body={
           "summary": summary,
           "description": desc,
           "start": {"dateTime": start.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
           "end": {"dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
       }
   ).execute()

   print("created event")
   print("id: ", event_result['id'])
   print("summary: ", event_result['summary'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])


def cancel_s():
    """
        Delete an event from your calendar.
    """
    service = get_calendar()
    event_id  = input("Please enter event ID to be cancelled : ")
    # event = service.events().get(calendarId='primary', eventId=eventId).execute()
    deleted_event = service.events().delete(calendarId='primary', eventId=event_id).execute()
    print("Event deleted")
    # logging.info('Event deleted: %s' % (event.get('htmlLink')))


def view_calendar():

    service = get_calendar()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 7 events\n')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=7, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'], event['id'])

    print()
"""
if __name__ == "__main__":

    print("Welcome to Code_Clinics\n")
    while True:
        print("What would you like to do?\nPress 1 for volunteer\nPress 2 to cancel volunteer slot\nPress 3 to view calendar\n")
        option = input("Please enter number : ")

        if option == '1':
            u_input()

        if option == '2':
            cancel_s()    

        if option == '3':
            view_calendar() 

        if option == 'off':
            break   

"""