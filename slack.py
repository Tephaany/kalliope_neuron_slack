from slackclient import SlackClient
import requests

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException, MissingParameterException

Slack_Actions = (
    "POST",
    "READ"
)


class Slack(NeuronModule):
    def __init__(self, **kwargs):

        super(Slack, self).__init__(**kwargs)

        # parameters
        self.action = kwargs.get('action', None)
        self.slack_token = kwargs.get('slack_token', None)
        self.channel = kwargs.get('slack_channel', None)
        self.message = kwargs.get('message', None)
        self.nb_messages = int(kwargs.get('nb_messages', 10))  # Int
        
        # check parameters
        if self._is_parameters_ok():
            sc = SlackClient(self.slack_token)

            if self.action == Slack_Actions[0]:  # POST
                if self._is_post_parameters_ok():

                    sc.api_call(
                        "chat.postMessage",
                        channel=self.channel,
                        text=self.message,
                        as_user=True
                    )

                    message = {
                        "action": self.action,
                        "text": self.message,
                        "channel": self.channel
                    }

            if self.action == Slack_Actions[1]:  # READ
                if self.is_read_parameters_ok():
                    # TODO get the list of channel
                    # user_list = sc.api_call("users.list")
                    #
                    # user_message_list = list()
                    #
                    # message = {
                    #     "action": self.action,
                    #     "messages": user_message_list,
                    #     "channel": self.channel
                    # }
                    pass

            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron.
        :return: True if parameters are ok, raise an exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.slack_token is None:
            raise MissingParameterException("Slack needs a slack_token")
        if self.action is None:
            raise MissingParameterException("Slack needs an action parameter")
        return True

    def _is_post_parameters_ok(self):
        """
        Check if parameters required to POST a message are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.channel is None:
            raise MissingParameterException("Slack needs a slack_channel")
        if self.message is None:
            raise MissingParameterException("Slack needs a message")
        
        return True

    def is_read_parameters_ok(self):
        """
        Check if parameters required to READ a message are present.
        :return: True, if parameters are OK, raise exception otherwise.

        .. raises:: MissingParameterException
        """
        if self.channel is None:
            raise MissingParameterException("Slack needs a slack_channel")

        return True




