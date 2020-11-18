import sys
#import config
import events_manager.bookings as bookings
import credentials.credentials as credentials
import events_manager.view as calendar

def cli_start():
    pass 

def check_arguments():
    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2:

        if sys.argv[1] == "help":
            return get_help()

        elif sys.argv[1] == "event":
            return calendar.main()

        elif sys.argv[1] == "login":
            return credentials.getCredentials()

        else:
            print("Please enter valid command")
            return get_help()


def get_help():
    print("""These are the Google calendar commands that can be used in various situations:
        
Setup and Login
        login                  Creates the config file that will be used 

Scheduling Events
        view events            View available events
        volunteer              volunteer for event
        cancel volunteering    cancellation of volunteering
        sign-up                sign-up for a volunteered event
        cancel event           cancels event booking made by student
""")


def get_event():

    print("ifejf")



check_arguments()