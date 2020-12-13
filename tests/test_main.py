import unittest
import cli
import sys
import unittest
from io import StringIO
from test_base import run_unittests
from test_base import captured_io



class TestAcceptance(unittest.TestCase):

    def test_help_fx(self):
        pass
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




if __name__ == '__main__':
    unittest.main()
