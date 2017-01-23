import unittest

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.slack.slack import Slack


class TestSlack(unittest.TestCase):

    def setUp(self):
        self.slack_token="kalliokey"
        self.channel = "kalliochannel"
        self.message = "kalliomessage"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Slack(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing message
        parameters = {
            "slack_token": self.slack_token,
            "channel": self.channel,
        }
        run_test(parameters)

        # missing slack_token
        parameters = {
            "channel": self.channel,
            "message": self.message
        }
        run_test(parameters)

        # missing channel
        parameters = {
            "slack_token": self.slack_token,
            "message": self.message
        }
        run_test(parameters)