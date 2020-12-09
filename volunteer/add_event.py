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


