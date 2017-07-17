# /usr/bin/python3

import time
import settings

from slackclient import SlackClient
from Functions.general import repeatcommand
from Functions.howabout import islive
from Functions.howabout import islivetogoogle


# starterbot's ID as an environment variable
BOT_ID = settings.BOT_ID
TOKEN = settings.LACK_BOT_TOKEN

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
REPEAT_COMMAND = "repeat"
ISLIFE_COMMAND = "islive"

# instantiate Slack & Twilio clients
slack_client = SlackClient(TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith(REPEAT_COMMAND):
        response = repeatcommand(command)
    elif command.startswith(ISLIFE_COMMAND):
        commandList = command.split(' ')
        if len(commandList) > 1:
            if islive(commandList[1]):
                response = "{} is alive".format(commandList[1])
            else:
                response = "ERROR: {} is not alive".format(commandList[1])
        else:
            if islivetogoogle():
                response = "We can connect 8.8.8.8"
            else:
                response = "ERROR: We cannot connect 8.8.8.8"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
