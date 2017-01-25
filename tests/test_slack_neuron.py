import unittest

import mock

from kalliope.core.NeuronModule import MissingParameterException
from kalliope.neurons.slack.slack import Slack


class TestSlack(unittest.TestCase):

    def setUp(self):
        self.action="POST"
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

        # Missing action
        parameters = {
            "slack_token": self.slack_token,
            "channel": self.channel,
        }
        run_test(parameters)

        # Mock the slackclient
        with mock.patch("slackclient.__init__") as mock_slackclient:
            # Mock the return value
            mock_slackclient.return_value = mock.Mock()

            # missing message
            parameters = {
                "action":self.action,
                "slack_token": self.slack_token,
                "channel": self.channel,
            }
            run_test(parameters)

            # missing slack_token
            parameters = {
                "action": self.action,
                "channel": self.channel,
                "message": self.message
            }
            run_test(parameters)

            # missing channel
            parameters = {
                "action": self.action,
                "slack_token": self.slack_token,
                "message": self.message
            }
            run_test(parameters)
