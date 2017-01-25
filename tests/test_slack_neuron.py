import json
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

    def test_get_list_messages(self):
        """
        Testing the _get_list_messages method
        """
        token = "testtoken"
        channel_id = "testchannelid"
        nb_messages = 3

        mocked_text = {
            "messages": [
                {"username": "Kalliope", "text": "hi"},
                      {"name": "MONF42", "text": "hi K"},
                      {"username": "Kalliope", "text": "how are you?"},
                      {"name": "MONF42", "text": "fine"},
                      {"username": "Kalliope", "text": "good"}
            ]
        }
        # Encode
        mocked_text = json.dumps(mocked_text, separators=(',', ':'))

        expected_result = [
            {"username": "Kalliope", "text": "hi"},
            {"name": "MONF42", "text": "hi K"},
            {"username": "Kalliope", "text": "how are you?"}
        ]

        with mock.patch("requests.post") as mock_requests_post:
            mock_requests_post.return_value = mock.Mock(status_code=200,
                                                        text=mocked_text)

            self.assertEqual(Slack._get_list_messages(token=token,
                                                      channel_id=channel_id,
                                                      nb_messages=nb_messages),
                             expected_result,
                             "Fail to get the proper number of messages")

    def test_get_channel_id(self):
        """
        Testing the _get_channel_id method
        """
        channel_name = "test"
        channel_list = {
            "channels": [
                {"id": 'CK88', "name": "kalliope"},
                {"id": 'OQY89', "name": "general"},
                {"id": '8OLK0', "name": "random"},
                {"id": 'MONF42', "name": "test"}
            ]
        }

        expected_result = 'MONF42'

        self.assertEqual(Slack._get_channel_id(channel_name=channel_name,
                                               channel_list=channel_list),
                         expected_result,
                         "Fail to get the channel ID ")

    def test_get_user_message_list(self):
        """
        Testing the _get_user_message_list method
        """
        user_list = {
            "members":[
                {"id": 'MONF42', "name": "monf"},
                {"id": 'BOT66', "name": "bot"},
                {"id": 'RDM90', "name": "myRandomUser"}
            ]
        }

        messages = [
            {"user": "MONF42", "text": "iam the test"},
            {"user": "BOT66", "text": "iam the bot"},
            {"user": "MONF42", "text": "hi bot"},
            {"username": "Kalliope", "text": "Hi everybody"}
        ]

        expected_result = [
            {"monf":"iam the test"},
            {"bot": "iam the bot"},
            {"monf": "hi bot"},
            {"Kalliope": "Hi everybody"}
        ]

        self.assertEquals(Slack._get_user_message_list(user_list=user_list,
                                                       messages=messages),
                          expected_result,
                          "Fail to deliver the user message")

