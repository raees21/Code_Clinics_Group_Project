import sys
import config


def cli_start():
    pass 

def check_arguments():
    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2:

        if var == "help":
            return get_help()

        elif var == "event":
            return view_calendar()

        elif var == "login":
            return get_calendar()

        else:
            print("Please enter valid command")
            return get_help()


def get_help():
    print("""These are the Google calendar commands that can be used in various situations:
        
setup and login
        login                  Creates the config file that will be used 

scheduling events
        view events            View available events
        volunteer              volunteer for event
        cancel volunteering    cancellation of volunteering
        sign-up                sign-up for a volunteered event
        cancel event           cancels event booking made by student
""")


def get_event():

    print("ifejf")



check_arguments()