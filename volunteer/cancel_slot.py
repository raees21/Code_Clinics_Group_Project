import calendar_setup.bookings as calendar

def cancel_s():
    global is_cancel

    is_cancel = True
    calendar.view_calendar()
    is_cancel = False

def cancel_slot(eventId):

    '''Function to delete/cancel event'''

    service = credentials.getCredentials()

    event = service.events().get(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()

    deleted_event = service.events().delete(calendarId='codeclinics00@gmail.com', eventId=eventId).execute()

    print("Event deleted")
