import sys
import os.path
#import config
#import events_manager.bookings as bookings
import user_credentials.credential as credentials
from student import bookings
from volunteers import bookings
import calendars.view as calendar
import student.student_info as student

def cli_start():
    pass 

def check_arguments(args = sys.argv):
    if len(args) == 1:
        return get_help()

    if len(args) == 2:

        if str(args[1]).lower() == "help":
            return get_help()

        elif str(args[1]).lower() == "events":
            return calendar.main()

        elif str(args[1]).lower() == "login":
            student.login_details()
            return credentials.getCredentials(), credentials.get_service_calendar()

        elif str(args[1]).lower() == "login2":
            return credentials.getCredentials()     
        
        elif sys.argv[1].lower() == "volunteer":

            with open ("login_info","r") as email:
                mail = email.readlines()
                v_mail = mail[1].replace("\n", "")
                # print(v_mail)

            conf = ""
            date = input("Date & Time : ")
            summary = input("Event Summary : ")
            description = input ("Event Description : ")
            creator = v_mail
            meet =  input("Would you like to set a google-meet (Y/N) : ")
           
            return bookings.add_event(date, summary, description, creator, meet)
        
        elif sys.argv[1] == "patient":

            with open ("login_info","r") as email:
                mail = email.readlines()
                p_mail = mail[1].replace("\n", "")

            calendar = bookings.view_calendar()
            slot = int(input("Please a slot number to book : "))
            patient = p_mail
            service = credentials.getCredentials()
            
            return update.addEventProperty(service, patient, slot, calendarId='c_79einr1qumsjbjatip5f9tfacs@group.calendar.google.com')

        elif args[1].lower() == "cancel":
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
