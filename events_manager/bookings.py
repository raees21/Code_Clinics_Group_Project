from datetime import time, timedelta, datetime, date
import datetime
import datefinder
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import user_credentials.credential as credentials


def u_input():
    '''Taking in user input for creating an event'''
 
    print("Adding an event ... ")
    summary = input("Event (ie 'code_clinic') : ")
    start_time = input("Date & Time (ie 25 Jul 13.30pm ) : ")
    desc = input("Topic of speciality : ")
    add_event(start_time, summary, desc)

    return summary, start_time, desc
    

def add_event(start_time, summary, desc, creator):
   
    service = credentials.getCredentials()
    timer = list(datefinder.find_dates(start_time))

    if len(timer):
        start = timer[0]
        end = start + timedelta(minutes = 30)

    event_result = service.events().insert(calendarId="c_nf7rjg7u6b3hchbgi670hfqca4@group.calendar.google.com",
        body={
            "summary": summary,
            "description": desc,
            "start": {"dateTime": start.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
            "end": {"dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
            'attendees': [{'email': creator}],
        }
    ).execute()
    

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])



def cancel_s(eventId):
    """
        Delete an event from your calendar.
    """
    service = credentials.getCredentials()

    event = service.events().get(calendarId='c_nf7rjg7u6b3hchbgi670hfqca4@group.calendar.google.com', eventId=eventId).execute()

    deleted_event = service.events().delete(calendarId='c_nf7rjg7u6b3hchbgi670hfqca4@group.calendar.google.com', eventId=eventId).execute()

    print("Event deleted")
    # logging.info('Event deleted: %s' % (event.get('htmlLink')))


def view_calendar():

    service = credentials.getCredentials()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 7 events\n')
    events_result = service.events().list(calendarId='c_nf7rjg7u6b3hchbgi670hfqca4@group.calendar.google.com', timeMin=now,
                                        maxResults=7, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_id = []

    current_date = date.today()
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        new_date_str = str(new_date)

        for i, event in enumerate(events):
            date1 = event['start'].get('dateTime').split('T')[0]

            if date1 == new_date_str:
                start_time = event['start'].get('dateTime').split('T')[1].split('+')[0]
                end_time = event['end'].get('dateTime').split('T')[1].split('+')[0]
                organizer = event['creator'].get('email')

                if 'attendees' in event and 'hangoutLink' not in event:
                    attendee_list = []
                    attendees = event["attendees"]

                    for attendee in attendees:
                        attendee_list.append(attendee['email'])
                    new = " ,".join(attendee_list)
                    event_sum = event["summary"]
                    event_id.append(event['id'])
                    print(f"{i}. {date1} {organizer} {start_time} {end_time} {event_sum} {new} No Meet Link")


                elif 'attendees' not in event and 'hangoutLink' in event:
                    meet_link = event["hangoutLink"]
                    event_sum = event["summary"]
                    event_id.append(event['id'])
                    print(f"{i}. {date1} {organizer} {start_time} {end_time} {event_sum} No Attendees Currently  {meet_link}")


                elif 'attendees' in event and 'hangoutLink' in event:
                    attendee_list = []
                    attendees = event["attendees"]

                    for attendee in attendees:
                        attendee_list.append(attendee['email'])
                    new = " ,".join(attendee_list)

                    meet_link = event["hangoutLink"]
                    event_sum = event["summary"]
                    event_id.append(event['id'])
                    print(f"{i}. {date1} {organizer} {start_time} {end_time} {event_sum} {new}  {meet_link}")

                else:
                    event_sum = event["summary"]
                    event_id.append(event['id'])
                    print(f"{i}. {date1} {organizer} {start_time} {end_time} {event_sum} No Attendees Currently  No Meet Link")

                print("")    


    event_id_cancel  = int(input("Please enter event number to be cancelled : "))

    return cancel_s(event_id[event_id_cancel])


