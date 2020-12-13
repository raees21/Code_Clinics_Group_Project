import sys
import os.path
import calendar_setup.bookings as bookings
import calendar_setup.view as view
import credential as credentials
import calendar_setup
import login_details

args = sys.argv

def check_arguments(args):
    """"""

    if len(args) == 1:
        return get_help()

    if len(args) == 2 and args[1] == "login":
        
        login_details.login_func()
        
        return credentials.getCredentials()


    if (len(args) == 2 or len(args) == 3) and os.path.exists('login_info'):
        
        if args[1] == "help":
            return get_help()

        elif args[1] == "events":
            if len(args) == 2:
                return view.main()
            if len(args) == 3:
                return calendar_setup.view.day_details(str(args[2]))

        elif args[1] == "volunteer" and "cancel" in args :
            return bookings.volunteer_cancel_slot()

        elif args[1] == "patient" and "cancel" in args :
            print('patient cancellation\n') 

            with open ("login_info","r") as email:
                mail = email.readlines()
                p_mail = mail[1].replace("\n", "")

            calendar = bookings.view_calendar()
            slot = int(input("Please select a slot number to cancel : "))
            patient = p_mail
            service = credentials.getCredentials()

            return bookings.patient_cancel(service, slot,calendarId='codeclinics00@gmail.com')   

        elif args[1] == "volunteer":

            with open ("login_info","r") as email:
                mail = email.readlines()
                v_mail = mail[1].replace("\n", "")

            conf = ""
            date = input("Date & Time (12 jan 12.30pm): ")
            summary = input("Event Summary : ")
            description = input ("Event Description : ")
            creator = v_mail
            meet =  input("Would you like to set a google-meet (Y/N)? : ")
           
            return bookings.volunteer_slot(date, summary, description, creator, meet)
        
        elif args[1] == "patient":

            with open ("login_info","r") as email:
                mail = email.readlines()
                p_mail = mail[1].replace("\n", "")

            calendar = bookings.view_calendar()
            slot = int(input("Please select a slot number to book : "))
            patient = p_mail
            service = credentials.getCredentials()
            
            return bookings.join_event(service, patient, slot, calendarId='codeclinics00@gmail.com')

        else:
            print("Please enter valid command")
            return get_help()
    else:
        print('Please login using')
        print('')
        print('    cli login')

def get_help():
    """
    Provides help information to the user
    """

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

check_arguments(args)
