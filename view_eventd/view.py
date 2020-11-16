from __future__ import print_function
from datetime import time, timedelta, datetime, date
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

ini_time_for_now = datetime.datetime.now()


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
                                        
    events = events_result.get('items', [])
    
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
                print(start_time,'\t', end_time,'\t', event['summary'])
        print('\n')

if __name__ == '__main__':
    main()