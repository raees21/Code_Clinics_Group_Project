from datetime import time, timedelta, datetime, date
import volunteer.cancel_slot as cancel
import datetime
import datefinder
import pickle
import os.path
from uuid import uuid4
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import credential as credential

event_id = []
is_cancel = False

def view_calendar():

    global event_id, is_cancel

    service = credential.getCredentials()
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

    if is_cancel :

        event_id_cancel  = int(input("Please enter event number to be cancelled : "))

        return cancel.cancel_slot(event_id[event_id_cancel])

    return event_id
