from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']
#SCOPES = ['https://calendar.google.com/calendar/u/0?cid=Y19uZjdyamc3dTZiM2hjaGJnaTY3MGhmcWNhNEBncm91cC5jYWxlbmRhci5nb29nbGUuY29t']

def getCredentials():
    """
        Get user credentials from Google Calendar API
        For more informations, go to :
            https://developers.google.com/calendar/quickstart/python

            x Input : json secret client file obtained with GC API
            X Output : the obtained credentials
    """
    creds = None
    path = os.path.expanduser('~/')
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(path + '.token.pickle'):
        with open(path + '.token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_163834025851-92js5g5aqpb8h8etbmukuu9uhv8t563u.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(path + '.token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

