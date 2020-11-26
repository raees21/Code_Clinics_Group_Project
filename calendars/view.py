from __future__ import print_function
from datetime import time, timedelta, datetime, date
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import user_credentials.credential as credentials
from tabulate import tabulate

ini_time_for_now = datetime.datetime.now()


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():

    service = credentials.getCredentials()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='c_nf7rjg7u6b3hchbgi670hfqca4@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
                                        
    events = events_result.get('items', [])
    
    current_date = date.today()

    table = []
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        table.append([new_date, "Events for the day listed below", "----------", "----------", "------------------------", "--------------------", "---------------"])
        #table.append([])
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

                table.append([])       

            else:
                table.append([]) 


    print(tabulate(table, ["\u001b[1m Date \u001b[0m", "\u001b[1m Organizer \u001b[0m", "\u001b[1m Start Time \u001b[0m", "\u001b[1m End Time \u001b[0m", "\u001b[1m Summary \u001b[0m", "\u001b[1m Attendees \u001b[0m", "\u001b[1m Google Meet Link \u001b[0m"], tablefmt="fancy_grid"))


if __name__ == '__main__':
    main()