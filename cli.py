import sys
import config


options = {"help" : ['usable commands','exit'], "event" : ["delete event", "schedule event"], "login": ["login"]}

def cli_start():
    pass 

def check_arguments():
    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2:
        for x,y in options.items():
            if sys.argv[1] == x:
             var = x

        if var == "help":
            return get_help()

        elif var == "event":
            return config.view_calendar()

        elif var == "login":
            return config.get_calendar()

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