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

    service = credentials.getCredentials()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='c_79einr1qumsjbjatip5f9tfacs@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
                                        
    events = events_result.get('items', [])
    print(type(events))
    print(events)
    # for k, info in events.items():
    #     print("key")
    #     for key in info:
    #         print(key + ":", info(key))
    
    current_date = date.today()
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        print(new_date.strftime("%c"))
        print('---------------------------------------------') # Anza
        print('Start  '  , '\t', 'End    ', '\t', 'Details')
        print('-------', '\t', '-------', '\t', '-------')
        new_date_str = str(new_date)
        for event in events:
            date1 = event['start'].get('dateTime').split('T')[0]
            if date1 == new_date_str:
                start_time = event['start'].get('dateTime').split('T')[1].split('+')[0]
                end_time = event['end'].get('dateTime').split('T')[1].split('+')[0]
                organizer = event['organizer'].get('email')
                #meets_link = event['conferenceData'].get('entryPoints').get('uri')
                print(start_time,'\t', end_time,'\t', event['summary'],'\t','\t',organizer, "\t", '\t')
        print('\n')

    table = []
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        table.append([new_date, "Events for the day listed below", "********", "********", "*********"])
        #table.append([])
        new_date_str = str(new_date)
        for event in events:
            date1 = event['start'].get('dateTime').split('T')[0]
            if date1 == new_date_str:
                    print(event)
                    print("")
                    start_time = event['start'].get('dateTime').split('T')[1].split('+')[0]
                    end_time = event['end'].get('dateTime').split('T')[1].split('+')[0]
                    organizer = event['creator'].get('email')
                    # attendees = event['attendees']
                    # print(attendees)
                    if 'attendees' in event:
                        attendee_list = []
                        attendees = event["attendees"]
                        #print(attendees)
                        for attendee in attendees:
                            attendee_list.append(attendee['email'])
                        new = " ,".join(attendee_list)
                        table.append([date1, organizer, start_time, end_time, event["summary"],new])
                    else:
                        table.append([date1, organizer, start_time, end_time, event["summary"],"Booking available"])
        table.append([])
            
    #print(table)
    #rint(tabulate(table))
    print(tabulate(table, ["date", "organizer", "start time", "end time", "summary", "attendees"], tablefmt="fancy_grid"))
    #print(tabulate(["organizer", "attendee", "date" , "start time", "end time", "details"]))

if __name__ == '__main__':
    main()