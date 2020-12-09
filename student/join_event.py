import calendar_setup

def addEventProperty(service, patient, eventId,calendarId='codeclinics00@gmail.com'):
    
    event_id = calendar_setup.event_id
    
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
