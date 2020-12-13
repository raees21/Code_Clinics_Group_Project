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
import credential as credential


#Declaration of globals that will be used
event_id = []
is_cancel = False

def read_file():
    """
    Opening and reading userdata file
    """

    with open ("login_info","r") as email:
        mail = email.readlines()
        p_mail = mail[1].replace("\n", "")

    admin = p_mail
    return admin    

def volunteer_slot(start_time, summary, desc, creator, meet):
    """Function for volunteer to create a slot
    :param start_time: The date, in the format (dd mm event_time)
    :param summary: Title of the event
    :param desc: Description of the event
    :param creator: The creator of the event
    :param meet: Google meet link of the event
    """

    try:
        service = credential.getCredentials()#Calling calendar service
        timer = list(datefinder.find_dates(start_time))
        conference = ''
        ah = str(timer[0])
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10,singleEvents=True,
                                            orderBy='startTime').execute()

        events = events_result.get('items', [])
        current_date = date.today()
        i = 0
        while i < 7:
            new_date = current_date + timedelta(days = i)
            new_date_str = str(new_date)
            
            for event in events:
                (date_1, start_time) = event['start'].get('dateTime').split('T')
                start_time = start_time.split('+')
                start_time_d = date_1 +' ' + start_time[0]
                if ah == start_time_d:
                    print('Slot booked try another slot')
                    datee = input("Date & Time (12 jan 12.30pm): ")
                    summary = input("Event Summary : ")
                    description = input ("Event Description : ")
                    meet =  input("Would you like to set a google-meet (Y/N) : ")
                    timer = list(datefinder.find_dates(datee))
                    ah = str(timer[0])
                    i = -1
                    break
            i+=1

        #Condition to include a google-meets link           
        if meet.lower() == "y":
            conference = {"createRequest": {"requestId": f"{uuid4().hex}","conferenceSolutionKey": {"type": "hangoutsMeet"}}}

        if meet.lower() == "n":
            conference = None    
        
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
                "conferenceData" : conference,
            },conferenceDataVersion=1
        ).execute()
        print("created event")
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    except:
        print("\nOops...Invalid input. Try again\n")


def join_event(service, patient, eventId,calendarId='codeclinics00@gmail.com'):
    """Function for the patient to book a slot
    :param service: authentication and authorization of the api
    :param patient: user that needs to book for the event
    :param eventId: event identifier
    :param calendaId: calendar identifier
    """

    try:
        id = event_id[eventId]
        event = service.events().get(calendarId=calendarId, eventId=id).execute()
        creator = event["attendees"]
        
        #Condition to check if the slot is booked
        if len(creator) == 2:
            print("\nEvent fully booked, try another slot\n")

        else:
            for i in creator:
                creator = creator[0]
                creator = creator['email']

                event["attendees"] = [{'email': creator},{'email' : patient}]
                updated_event = service.events().update(calendarId=calendarId, eventId=id, body=event).execute()
                
                print(updated_event['updated'])
                print("success")
    except:
        print("\nInvalid slot...Please try again\n")    


def volunteer_cancel_slot():
    """
    Cancelling of a volunteered slot
    """

    global is_cancel

    is_cancel = True
    view_calendar()
    is_cancel = False


def cancel_slot(eventId):
    """
    Function to delete/cancel event
    :param eventId: event identifier
    """
    try:
        service = credential.getCredentials()
        admin = read_file()
        event = service.events().get(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()
        attendee = event["attendees"]
        creator = attendee[0]
        creator = creator["email"]
        
        '''Condition to check if there is a subscription to the slot'''
        if creator != admin :
            print("\nCannot delete event you did not create\n")

        elif len(attendee) == 2:
            print("\nCannot delete before consultation\n")

        else:
            deleted_event = service.events().delete(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()
            print("\nEvent deleted\n")

    except:
        print("\nInvalid slot...Please try again\n")        


def patient_cancel(service,eventId,calendarId='codeclinics00@gmail.com'):
    """Cancellation of a slot booked by patient
    :param service:  authentication and authorization of the api
    :param eventId: event identifier
    :param calendarId calendar identifier
    """

    try:
        admin = read_file()
        id = event_id[eventId]
        event = service.events().get(calendarId=calendarId, eventId=id).execute()
        creator = event["attendees"]
        creator_vul = creator[0]
        creator_vul = creator_vul['email']

        if len(creator) == 2:
            patient_can = creator[1]
            patient_can = patient_can['email']
            print(patient_can)

            if patient_can != admin:
                print("\ncannot cancel slot you did not create\n")

            else:
                event["attendees"] = [{'email' : creator_vul}]
                updated_event = service.events().update(calendarId=calendarId, eventId=id, body=event).execute()
                print(updated_event['updated'])
                print("success")
               

        else:
            print('No slot available to cancel')
             
    except:
        print("\nInvalid slot...Please try again\n")   


def view_calendar():
    """
    Function to view calendar
    """

    global event_id

    service = credential.getCredentials()
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 7 events\n')
    events_result = service.events().list(calendarId='codeclinics00@gmail.com', timeMin=now,
                                        maxResults=7, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
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

    if is_cancel :
        try:
            event_id_cancel  = int(input("Please enter event number to be cancelled : "))
            return cancel_slot(event_id[event_id_cancel])
        except:
            print("\nInvalid slot...Please try again\n")   

    return event_id
