import sys
import os.path
#import config
import events_manager.bookings as bookings
import events_manager.view as calendar
import credential as credentials
import events_manager.view as calendar
import events_manager.bookings as update
import events_manager


def cli_start():
    pass 


def check_arguments(args=sys.argv):
    if len(args) == 1:
        return get_help()

    if len(args) == 2:

        if args[1] == "help":
            return get_help()

        elif args[1] == "events":
            return events_manager.view.main()

        elif args[1] == "login":
            return credentials.getCredentials()
        
        elif args[1] == "volunteer":
            conf = ""
            date = input("Date & Time : ")
            summary = input("Event Summary : ")
            description = input ("Event Description : ")
            creator = input("Volunteer Email : ")
            meet =  input("Would you like to set a google-meet (Y/N) : ")
           
            return bookings.add_event(date, summary, description, creator, meet)

        elif args[1] == "patient":

            calendar = bookings.view_calendar()
            slot = int(input("Please a slot number to book : "))
            patient = input("Patient email : ")
            service = credentials.getCredentials()
            
            return update.addEventProperty(service, patient, slot, calendarId='codeclinics00@gmail.com')


        elif args[1] == "cancel":
            return bookings.view_calendar()

        else:
            print("Please enter valid command")
            return get_help()

    if len(args) == 3:
        if args[1] == "events":
            return events_manager.view.day_details(str(sys.argv[2]))


def get_help():
    print("""These are the Google calendar commands that can be used in various situations:
        
Setup and Login
        login                  Creates the config file that will be used 

Scheduling Events
        events                 View available events
        volunteer              volunteer for event
        cancel                 cancellation of volunteering
        sign-up                sign-up for a volunteered event
        cancel event           cancels event booking made by student
""")


def get_event():

    print("ifejf")



check_arguments()