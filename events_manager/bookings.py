from datetime import time, timedelta, datetime, date
import datetime
import datefinder
import pickle
import os.path
from uuid import uuid4
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import credential as credentials

event_id = []

def u_input():
    '''Taking in user input for creating an event'''
 
    print("Adding an event ... ")
    summary = input("Event (ie 'code_clinic') : ")
    start_time = input("Date & Time (ie 25 Jul 13.30pm ) : ")
    desc = input("Topic of speciality : ")
    add_event(start_time, summary, desc)

    return summary, start_time, desc
    

def add_event(start_time, summary, desc, creator, meet):
   
    service = credentials.getCredentials()
    timer = list(datefinder.find_dates(start_time))

    '''ADDS MEETS link'''
    conf = ''

    if meet.lower() == "y":

        conf = {"createRequest": {"requestId": f"{uuid4().hex}","conferenceSolutionKey": {"type": "hangoutsMeet"}}}

    if meet.lower() == "n":
        conf = None    
    
    '''end of meets condition'''

    if len(timer):
        start = timer[0]
        end = start + timedelta(minutes = 90)

    event_result = service.events().insert(calendarId="codeclinics00@gmail.com",
        body={
            "summary": summary,
            "description": desc,
            "start": {"dateTime": start.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
            "end": {"dateTime": end.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'CAT'},
            "attendees": [{'email': creator}],
            "conferenceData" : conf,
        },conferenceDataVersion=1
    ).execute()
    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])


def addEventProperty(service, patient, eventId,calendarId='codeclinics00@gmail.com'):
    global event_id
    
    '''Start event joining'''
    id = event_id[eventId]
    
    event = service.events().get(calendarId=calendarId, eventId=id).execute()
    creator = event["attendees"]

    for i in creator:
        creator = creator[0]
        creator = creator['email']

    event["attendees"] = [{'email': patient},{'email' : creator}]
    updated_event = service.events().update(calendarId=calendarId, eventId=id, body=event).execute()

    
    print(updated_event['updated'])
    print("success")
'''end event joining'''

def cancel_s(eventId):
    """
        Delete an event from your calendar.
    """
    service = credentials.getCredentials()

    event = service.events().get(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()

    deleted_event = service.events().delete(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()

    print("Event deleted")

def view_calendar():

    global event_id

    service = credentials.getCredentials()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 7 events\n')
    events_result = service.events().list(calendarId='codeclinics00@gmail.com', timeMin=now,
                                        maxResults=7, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # event_id = []

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

                    if organizer == "mtshishi@student.wethinkcode.co.za":
                        print(f"{i}. {date1} {organizer} {start_time} {end_time} {event_sum} {new} No Meet Link")

                    else:
                        print("No events ")



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


    # event_id_cancel  = int(input("Please enter event number to be cancelled : "))

    # return cancel_s(event_id[event_id_cancel])

    return event_id
