from datetime import time, timedelta, datetime, date
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def view_grid():

    day_keys = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_times = []
    #for j in range(8, 18):
    #    day_times.append(time(j, 00))
        #print(f"* {time(j, 00)} * ")

    #print(day_times)
    
    #for i in range(8,16):
    a = datetime.now()
    #    get_times.append(a)

    #print(get_times)
    #print(a)

    b =  a + timedelta(hours = 1) 

    #print(b)


def print_grid():

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

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 7 events\n')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=7, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    event_times = []
    event_summary = []
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event['summary']

        event_times.append(start)
        event_summary.append(summary)

        print(start)#, event['summary'], event['id'])

    print(event_times)
    print(event_summary)

    current_date = date.today()

    print("************************************************************************************************")
    for i in range(7):
        new_date = current_date + timedelta(days = i)
        print(" "+str(new_date), end = " "*3)
    print("")
    print("************************************************************************************************")
    for i in range(8, 18):
        for j in range(7):
            new_date = current_date + timedelta(days = j)

            print(f"* {time((i), 00)} * ", end=" ")
            for k in range(len(event_times)):
                if str(new_date) == str(event_times[k][:10]):
                    
                    print(event_summary[k])

        print("")
        print("*          *  *          *  *          *  *          *  *          *  *          *  *          *")
        print("*          *  *          *  *          *  *          *  *          *  *          *  *          *")
        print("*          *  *          *  *          *  *          *  *          *  *          *  *          *")

    print("************************************************************************************************`")



view_grid()
print_grid()
