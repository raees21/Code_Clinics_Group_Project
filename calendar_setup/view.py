from __future__ import print_function
from datetime import time, timedelta, datetime, date
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import credential as credentials
from tabulate import tabulate

ini_time_for_now = datetime.datetime.now()


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """
    get the overall calendar of the up-coming 7 days
    """

    service = credentials.getCredentials()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='codeclinics00@gmail.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
                                        
    events = events_result.get('items', [])
    
    current_date = date.today()

    table = []
    """
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        table.append([new_date, "Events for the day listed below", "----------", "----------", "------------------------", "--------------------", "---------------"])
        table.append([])
        new_date_str = str(new_date)
        for event in events:

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
                    table.append([date1, organizer, start_time, end_time, event["summary"],new, "No Meet Link"])    


                elif 'attendees' not in event and 'hangoutLink' in event:
                    meet_link = event["hangoutLink"]
                    table.append([date1, organizer, start_time, end_time, event["summary"],"No Attendees Currently", meet_link])


                elif 'attendees' in event and 'hangoutLink' in event:
                    attendee_list = []
                    attendees = event["attendees"]

                    for attendee in attendees:
                        attendee_list.append(attendee['email'])
                    new = " ,".join(attendee_list)

                    meet_link = event["hangoutLink"]
                    table.append([date1, organizer, start_time, end_time, event["summary"],new, meet_link])


                else:
                    table.append([date1, organizer, start_time, end_time, event["summary"],"Booking available", "No Meet Link"])

        table.append(["----------", "------------------------------------------------------", "----------", "----------", "------------------------", "--------------------", "---------------"])

    #print(table)

    print(tabulate(table, ["Date", "Organizer", "Start Time", "End Time", "Summary", "Attendees", "Google Meet Link"], tablefmt="simple"))
    """

    event_list = []
    day_list = []

    for i in range(7):
        new_date = current_date + timedelta(days = i)
        new_date_str = str(new_date)
        temp_list_day = []
        day_list.append(i)
 
        for event in events:
            temp_list = []
            date1 = event['start'].get('dateTime').split('T')[0]

            if date1 == new_date_str:

                start_time = event['start'].get('dateTime').split('T')[1].split('+')[0]
                end_time = event['end'].get('dateTime').split('T')[1].split('+')[0]
                organizer = event['creator'].get('email')

                temp_list.append(date1)
                temp_list.append(organizer)
                temp_list.append(start_time)
                temp_list.append(end_time)
                temp_list.append(event['summary'])

                if 'hangoutLink' in event:
                    meet_link = event["hangoutLink"]
                    temp_list.append(meet_link)
                else:
                    meet_link = "No Meet Link Available"
                    temp_list.append(meet_link)

                if 'attendees' in event:
                    attendee_list = []
                    attendees = event["attendees"]

                    for attendee in attendees:
                        attendee_list.append(attendee['email'])
                    new = " ,".join(attendee_list)
                    temp_list.append(new)
                else:
                    new = "No Attendees Currently"                    
                    temp_list.append(new)

                temp_list_day.append(temp_list)

        if temp_list_day != []:
            event_list.append(temp_list_day)

    #print(event_list)

    date_list = []
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        new_date_str = str(new_date)
        date_list.append(new_date_str)

        for event in events:
            date1 = event['start'].get('dateTime').split('T')[0]
            start_time = event['start'].get('dateTime').split('T')[1].split('+')[0]
            end_time = event['end'].get('dateTime').split('T')[1].split('+')[0]

    time_list = ['08:00:00', '08:30:00', '09:00:00', '09:30:00', '10:00:00', '10:30:00', '11:00:00',
                '11:30:00', '12:00:00', '12:30:00', '13:00:00', '13:30:00', '14:00:00',
                '14:30:00', '15:00:00', '15:30:00', '16:00:00', '16:30:00', '17:00:00']

    event_details = []
    

    for i in range(len(time_list)):
        event_details.append([time_list[i], "Book Now", "Book Now", "Book Now", "Book Now", "Book Now", "Book Now", "Book Now"])

    for k in range(len(date_list)):
        for i in range(len(event_list)):
            for j in range(len(event_list[i])):
                if str(event_list[i][j][0]) == str(date_list[k]):
                    event_list_split = str(event_list[i][j][0]).split('-')
                    current_date_split = str(current_date).split('-')
                    date_index = int(event_list_split[2]) - int(current_date_split[2])  + 1
                    for x in range(len(event_details)):
                        if str(event_details[x][0]) == str(event_list[i][j][2]):
                            time_index = x
                            event_details[time_index][date_index] = event_list[i][j][4]
                            event_details[time_index+1][date_index] = event_list[i][j][4]
                            event_details[time_index+2][date_index] = event_list[i][j][4]


                    
    #print(event_details)
    print("")
    print(tabulate(event_details, ["Time", date_list[0], date_list[1], date_list[2], date_list[3], date_list[4], date_list[5],date_list[6]], tablefmt="fancy_grid"))
    #print(event_list)
    return event_details, date_list, event_list
    #print(date_list)

def day_details(date):
    """
    give overall events for the day
    :param date: The date, in the format "yyyy-mm-dd" gets the event for the whole day
    """

    event_details, date_list, event_list = main()

    #new_event_list = []
    new_event_list_day = []

    for i in range(len(event_list)):
        for j in range(len(event_list[i])):
            if str(date) == str(event_list[i][j][0]):
                new_event_list = []
                new_event_list.append(event_list[i][j][0])
                new_event_list.append(event_list[i][j][1])
                new_event_list.append(event_list[i][j][2])
                new_event_list.append(event_list[i][j][3])   
                new_event_list.append(event_list[i][j][4])
                new_event_list.append(event_list[i][j][5])
                new_event_list.append(event_list[i][j][6])
                new_event_list_day.append(new_event_list)

    #print(event_list)
    print("")
    #print(new_event_list_day)
    print(tabulate(new_event_list_day, ["Date", "Organizer", "Start Time", "End Time", "Summary", "Google Meet Link", "Attendees"], tablefmt="fancy_grid"))
    print("")          
