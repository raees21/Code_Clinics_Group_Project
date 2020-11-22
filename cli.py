import sys
import os.path
#import config
import events_manager.bookings as bookings
import events_manager.view as calendar
import credential as credentials
import events_manager.view as calendar

def cli_start():
    pass 

def check_arguments():
    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2:

        if sys.argv[1] == "help":
            return get_help()

        elif sys.argv[1] == "events":
            return calendar.main()

        elif sys.argv[1] == "login":
            return credentials.getCredentials()
        
        elif sys.argv[1] == "volunteer":
            date = input("Date & Time : ")
            summary = input("Event Summary : ")
            description = input ("Event Description : ")
            creator = input("Volunteer Email : ")
            return bookings.add_event(date, summary, description, creator)

        elif sys.argv[1] == "cancel":
            return bookings.view_calendar()

        else:
            print("Please enter valid command")
            return get_help()


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