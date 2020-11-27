import unittest
import sys
import cli
from io import StringIO
from test_base import captured_io
from test_base import run_unittests
from unittest.mock import patch
from contextlib import redirect_stderr, redirect_stdout
import os



class TestCli(unittest.TestCase):
    # @patch (sys.stdin, "python3 cli.py help")

    @patch ("sys.stdin", StringIO("karend\nkarend@student.wethinkcoe.co.za\nfakepassword") )
#     def test_check_arguments(self):
#             sys.stdout = StringIO()
#             cli.check_arguments(args=['cli.py', 'login'])
#             self.assertEqual(sys.stdout.getvalue()[:164],"""Please enter your username: karend
# Please enter your email: karend@student.wethinkcode.co.za
# please enter a password: fakepassword
# Getting the upcoming 10 events
# """)

    def test_check_arguments_fx(self):
        pass

    def test_help_fx(self):
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


if __name__ == '__main__' :
    unittest.main()