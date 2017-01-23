from slackclient import SlackClient

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException, MissingParameterException

class Slack(NeuronModule):
    def __init__(self, **kwargs):

        super(Slack, self).__init__(**kwargs)

        # parameters
        self.slack_token = kwargs.get('slack_token', None)
        self.channel = kwargs.get('slack_channel', None)
        self.message = kwargs.get('message', None)
        
        # check parameters
        if self._is_parameters_ok():
            sc = SlackClient(self.slack_token)

            sc.api_call(
                "chat.postMessage",
                channel=self.channel,
                text=self.message,
                as_user=True
            )

            self.say(self.message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """
        if self.slack_token is None:
            raise MissingParameterException("Slack needs a slack_token")
        if self.channel is None:
            raise MissingParameterException("Slack needs a slack_channel")
        if self.message is None:
            raise MissingParameterException("Slack needs a message")
        
        return True




