#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
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


def CheckUserExist(conf, filepath, user):
    if TrustUserExist(conf, filepath):
        conf.read(filepath)
        if user in conf['trustuser']:
            return True
        else:
            return False
    else:
        return False


def CheckUserExistAndGetID(conf, filepath, user):
    conf.read(filepath)
    if user in conf['userlist']:
        userid = conf['userlist'][user]
        return True, userid
    else:
        return False, 'user_error_6'


def ValueAuthority(authority):
    roles = "^([1-5]){1}$"
    if re.match(roles, authority):
        return True
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

    def UserListUpdate(self):
        sc = SlackClient(TOKEN)
        api_call = sc.api_call("users.list")
        if api_call.get('ok'):
            userlist = api_call.get('members')
            for user in userlist:
                if not user['deleted']:
                    self.conf.set('userlist', user['name'], user.get('id'))
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_1'
        else:
            return False, 'user_error_1'

    def AddUser(self, USER, authority):
        if not ValueAuthority(authority):
            return False, 'user_error_8'
        check, userID = CheckUserExistAndGetID(self.conf, self.filepath, USER)
        if (check is True and
                not CheckUserExist(self.conf, self.filepath, userID)):
            self.conf.set('trustuser', userID, authority)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_1'
        elif (check is True and
                CheckUserExist(self.conf, self.filepath, userID)):
            keyvalue = self.conf.getint('trusthost', userID)
            if keyvalue == 0:
                if self.UnmaskUser(USER) is True:
                    return True, 'user_success_2'
                else:
                    return False, 'user_error_4'
            return False, 'user_error_3'
        elif check is False:
            return False, 'user_error_7'
        else:
            return False, 'user_error'

    def RemoveHost(self, USER):
        check, userID = CheckUserExistAndGetID(self.conf, self.filepath, USER)
        if (check is True and
                CheckUserExist(self.conf, self.filepath, userID)):
            self.conf.remove_option('trustuser', userID)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_3'
        elif (check is True and
                not CheckUserExist(self.conf, self.filepath, userID)):
            return True, 'host_success_3'
        elif check is False:
            userfile = self.conf.read(self.filepath)
            userlist = userfile['userlist']
            usertrust = userfile['trustuser']
            for user in usertrust:
                if user not in userlist:
                    self.conf.remove_option('trustuser', userID)
                pass
        else:
            return False, 'user_error'

    def MaskHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, self.filepath, keyname):
            self.conf.set('trusthost', keyname, 'false')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_2'
        else:
            return False, 'host_error_4'

    def UnmaskHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, self.filepath, keyname):
            self.conf.set('trusthost', keyname, 'true')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_2'
        else:
            return False, 'host_error_4'

    def CheckHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, self.filepath, keyname):
            ksyvalue = self.conf.getboolean('trusthost', keyname)
            return True, "{}=> key:{} value:{}".format(HOST, keyname, ksyvalue)
        else:
            return False, 'host_error_4'

    def ListAllHost(self):
        for item in self.conf.items('trusthost'):
            print("Host: {}, isMask: {}".format(item[0], item[1]))


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
