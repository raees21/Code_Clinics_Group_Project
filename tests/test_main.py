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
        self.assertEqual(sys.stdout.getvalue(),"""
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




if __name__ == '__main__':
    unittest.main()
