import unittest
import cli
import sys
import unittest
from io import StringIO
from test_base import run_unittests
from test_base import captured_io



class TestAcceptance(unittest.TestCase):

    def test_help_fx(self):

        sys.stdout = StringIO()
        cli.check_arguments(args=['cli.py', 'help'])
        self.assertEqual(sys.stdout.getvalue(),"""These are the Google calendar_setup commands that can be used in various situations:
        
Setup and Login
        login                  Creates the config file that will be used 

Scheduling Events
        events                 View available events
        volunteer              volunteer for event
        volunteer cancel       cancellation of volunteering
        patient                sign-up for a volunteered event
        patient cancel         cancels event booking made by student


""")


    def test__volunteer_event_creation(self):

        with captured_io(StringIO("25 jan 2020 12.30pm\ntest1\ntest1\ny\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'volunteer'])
                output = out.getvalue().strip()
                self.assertTrue(output.find('created event') > -1)


    def test__volunteer_event_creation_time(self):

        with captured_io(StringIO("25 jan 2020 12.30pm\ntest1\ntest1\ny\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'volunteer'])
                output = out.getvalue().strip()
                self.assertTrue(output.find('starts at:  2020-01-25T12:00:00+02:00') > -1)


    def test__volunteer_event_end(self):

        with captured_io(StringIO("25 jan 2020 12.30pm\ntest1\ntest1\ny\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'volunteer'])
                output = out.getvalue().strip()
                self.assertTrue(output.find('ends at:  2020-01-25T13:30:00+02:00') > -1)


    def test__volunteer_event_summary(self):

        with captured_io(StringIO("25 jan 2020 12.30pm\ntest1\ntest1\ny\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'volunteer'])
                output = out.getvalue().strip()
                self.assertTrue(output.find('summary:  test1') > -1)


    def test__volunteer_event_delete(self):

        with captured_io(StringIO("7\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'volunteer', 'cancel'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Invalid slot...Please try again') > -1)


    def test_patient_event_creation(self):

        with captured_io(StringIO("7\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'patient'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Invalid slot...Please try again') > -1)


    def test_patient_event_cancel(self):

        with captured_io(StringIO("7\n")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'patient', 'cancel'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Invalid slot...Please try again') > -1)

 
    def test_view_calendar_Book(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Book Now') > -1)


    def test_view_calendar_Time(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Time') > -1)


    def test_view_calendar_slot(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('08:00:00') > -1)


    def test_view_full_calendar_meet(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events', '2020-12-18'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Google Meet Link') > -1)


    def test_view_full_calendar_attendees(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events', '2020-12-18'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Attendees') > -1)


    def test_view_full_calendar_Organizer(self):

        with captured_io(StringIO("")) as (out, err) :
                cli.check_arguments(args=['cli.py', 'events', '2020-12-18'])
                output = out.getvalue().strip()

                self.assertTrue(output.find('Organizer') > -1)


if __name__ == '__main__':
    unittest.main()
