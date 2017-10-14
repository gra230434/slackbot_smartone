#!/usr/bin/python3
# -*- coding: utf-8 -*-

import settings

from slackclient import SlackClient

TOKEN = settings.LACK_BOT_TOKEN
BOT_NAME = settings.BOT_NAME

slack_client = SlackClient(TOKEN)


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                a = "ID for {} is {}".formar(user['name'], user.get('id'))
                print(a)
            else:
                print("error")
    else:
        print("could not find bot user with the name " + BOT_NAME)
