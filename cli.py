import sys
import os.path
import calendar_setup.bookings as bookings
import calendar_setup.view as view
import credential as credentials
import calendar_setup
import login_details


def cli_start():
    pass 

def check_arguments():

    path = os.path.expanduser('~/')

    if len(sys.argv) == 1:
        return get_help()

    if len(sys.argv) == 2 and sys.argv[1] == "login":
        
        login_details.login_func()
        
        return credentials.getCredentials()


    if (len(sys.argv) == 2 or len(sys.argv) == 3) and os.path.exists(path +'.token.pickle'):
        
        if sys.argv[1] == "help":
            return get_help()

        elif sys.argv[1] == "events":
            if len(sys.argv) == 2:
                return view.main()
            if len(sys.argv) == 3:
                return calendar_setup.view.day_details(str(sys.argv[2]))


        elif sys.argv[1] == "login":
            return credentials.getCredentials()

        elif sys.argv[1] == "volunteer" and "cancel" in sys.argv :
            return bookings.volunteer_cancel_slot()

        elif sys.argv[1] == "patient" and "cancel" in sys.argv :
            print('patient cancel') 

            with open ("login_info","r") as email:
                mail = email.readlines()
                p_mail = mail[1].replace("\n", "")

            calendar = bookings.view_calendar()
            slot = int(input("Please a slot number to cancel : "))
            patient = p_mail
            service = credentials.getCredentials()

            return bookings.patient_cancel(service, slot,calendarId='codeclinics00@gmail.com')   

        elif sys.argv[1] == "volunteer":

            with open ("login_info","r") as email:
                mail = email.readlines()
                v_mail = mail[1].replace("\n", "")

            conf = ""
            date = input("Date & Time : ")
            summary = input("Event Summary : ")
            description = input ("Event Description : ")
            creator = v_mail
            meet =  input("Would you like to set a google-meet (Y/N) : ")
           
            return bookings.volunteer_slot(date, summary, description, creator, meet)
        
        elif sys.argv[1] == "patient":

            with open ("login_info","r") as email:
                mail = email.readlines()
                p_mail = mail[1].replace("\n", "")

            calendar = bookings.view_calendar()
            slot = int(input("Please a slot number to book : "))
            patient = p_mail
            service = credentials.getCredentials()
            
            return bookings.join_event(service, patient, slot, calendarId='codeclinics00@gmail.com')

        else:
            print("Please enter valid command")
            return get_help()


def get_help():
    print("""These are the Google calendar_setup commands that can be used in various situations:
        
Setup and Login
        login                  Creates the config file that will be used 

Scheduling Events
        events                 View available events
        volunteer              volunteer for event
        volunteer cancel       cancellation of volunteering
        patient                sign-up for a volunteered event
        patient cancel         cancels event booking made by student

""")

check_arguments()