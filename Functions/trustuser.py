#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import configparser

from slackclient import SlackClient

try:
    syspath = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir))
    sys.path.insert(0, syspath)
    from settings import LACK_BOT_TOKEN as TOKEN
except Exception, e:
    raise


def TrustUserExist(conf, filepath):
    conf.read(filepath)
    sections = conf.sections()
    if 'trustuser' in sections:
        return True
    else:
        return False


def UserListExist(conf, filepath):
    conf.read(filepath)
    sections = conf.sections()
    if 'userlist' in sections:
        return True
    else:
        return False
    pass


def CheckUserExist(conf, filepath, keyname):
    if TrustUserExist(conf, filepath):
        conf.read(filepath)
        if keyname in conf['trustuser']:
            return True
        else:
            return False
    else:
        return False


class UserCommandConf(object):
    """docstring for UserCommandConf"""
    def __init__(self, filename='trust.conf', ):
        super(UserCommandConf, self).__init__()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.filepath = os.path.join(self.dirpath, filename)
        self.conf = configparser.ConfigParser()
        readconfig = self.ReadConf()
        if readconfig[0] is not True:
            return readconfig[1]

    def ReadConf(self):
        if os.path.isfile(self.filepath):
            if (TrustUserExist(self.conf, self.filepath) and
                    UserListExist(self.conf, self.filepath)):
                return True, 'success'
            else:
                return False, 'user_error_2'
        else:
            return False, 'user_error_1'

    def UserListUpdate():
        sc = SlackClient(TOKEN)
        api_call = sc.api_call("users.list")
        if api_call.get('ok'):
            userlist = api_call.get('members')
        pass


def HostCommand(command):
    commandList = command.split(' ')
    userconfig = UserCommandConf()
    if commandList[1] is 'add':
        userconfig.UserListUpdate()
        return userconfig.AddHost(commandList[2])
    elif commandList[1] is 'remove':
        return userconfig.RemoveHost(commandList[2])
    elif commandList[1] is 'mask':
        return userconfig.MaskHost(commandList[2])
    elif commandList[1] is 'unmask':
        return userconfig.UnmaskHost(commandList[2])
    else:
        return userconfig.ListAllHost()


def main():
    pass


if __name__ == '__main__':
    main()
