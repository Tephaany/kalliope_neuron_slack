# Slack

## Synopsis

This neuron allows you to send a message to slack (channel or IM).

## Installation
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_slack.git
```

## Options

| parameter           | required | default | choices | comment                     |
|---------------------|----------|---------|---------|-----------------------------|
| slack_token         | yes      | None    |         | Team User token             |
| slack_channel       | yes      | None    |         | Slack channel or user       |
| message             | yes      | None    |         | the message to send         |
## Return Values

| Name    | Description                       | Type   | sample          |
|---------|-----------------------------------|--------|-----------------|
| message | The message which has been posted | string | coucou kalliopé |

## Synapses example

```
- name: "post-slack"
  neurons:
    - slack:
        slack_token: "MY_SECRET_TOKEN"
        slack_channel: "#general"
        args:
          - message
  signals:
    - order: "post on slack {{ message }}"
```

## Notes

In order to be able to post on Slack, you need to get a slack token (currently only *Tokens for testing* are supported). 

### How to get your Slack token (associated with one team)

1. Sign in your [Slack account](https://slack.com/signin)
2. Create a [test token](https://api.slack.com/docs/oauth-test-tokens)
6. Get your token (Keep it secret !)
7. Post your first message with this neuron !

### Send a IM message
You need to get the IM channel's ID.

 1. Go to [Slack user api test page](https://api.slack.com/methods/users.list/test) 
 2. Select the token for the team and click to the test method button
 3. Get the ID for the user  
 4. Go to [Slack im list api test page](https://api.slack.com/methods/im.list/test) 
 5. Select the token for the team and click to the test method button
 6. Get the IM channel's ID associated for this user (property user)
