import sys
import os.path
#import config
#import events_manager.bookings as bookings
import user_credentials.credential as credentials
from student import bookings
from volunteers import bookings
import calendars.view as calendar


def cli_start():
    pass 

def check_arguments():
    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2:

        if str(sys.argv[1]).lower() == "help":
            return get_help()

        elif str(sys.argv[1]).lower() == "events":
            return calendar.main()

        elif str(sys.argv[1]).lower() == "login":
            return credentials.getCredentials(), credentials.get_service_calendar()

        elif str(sys.argv[1]).lower() == "login2":
            return credentials.getCredentials()     
        
        elif str(sys.argv[1]).lower() == "volunteer":
            date = input("\u001b[1m Date & Time : ")
            summary = input("\u001b[1m Event Summary : ")
            description = input ("\u001b[1m Event Description : ")
            creator = input("\u001b[1m Volunteer Email : ")
            return bookings.add_event(date, summary, description, creator)

        elif sys.argv[1].lower() == "cancel":
            return bookings.view_calendar()

        else:
            print("Please enter a valid command")
            return get_help()


def get_help():
    print("""
\u001b[1m  \u001b[44m These are the Google calendar commands that can be used in various situations:\u001b[0m
        
\u001b[1m \u001b[4m Setup and Login \u001b[0m
        login                  Creates the config file that will be used 

\u001b[1m \u001b[4m Scheduling Events \u001b[0m
        events                 View available events
        volunteer              volunteer for event
        cancel                 cancellation of volunteering
        sign-up                sign-up for a volunteered event
        cancel event           cancels event booking made by student
""")


def get_event():

    print("ifejf")


if __name__ == "__main__":
    check_arguments()