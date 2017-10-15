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
except Exception:
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
        if user in conf.options['trustuser']:
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
        return False, 'user_error_7'


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
            return False, 'user_error_9'
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if (checklist is True and checktrust is not True):
            self.conf.set('trustuser', USER, "{},{}".format(userID, authority))
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_1'
        elif (checklist is True and checktrust is True):
            keyvalue = self.conf.get('trusthost', USER).split(',')
            if int(keyvalue[1]) == 0:
                if self.UnmaskUser(USER, authority)[0] is True:
                    return True, 'user_success_2'
                else:
                    return False, 'user_error_4'
            return False, 'user_error_3'
        elif checklist is False:
            return False, 'user_error_8'
        else:
            return False, 'user_error'

    def RemoveUser(self, USER):
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if (checklist is True and checktrust is True):
            self.conf.remove_option('trustuser', USER)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_3'
        elif (checklist is True and checktrust is not True):
            return True, 'host_success_3'
        elif checklist is False:
            userfile = self.conf.read(self.filepath)
            userlist = userfile.options('userlist')
            usertrust = userfile.options('trustuser')
            for user in usertrust:
                if user not in userlist:
                    self.conf.remove_option('trustuser', user)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_5'
        else:
            return False, 'user_error'

    def ChageUser(self, USER, authority):
        if not ValueAuthority(authority):
            return False, 'user_error_9'
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if checklist is True and checktrust is True:
            self.conf.set('trustuser', USER, "{},{}".format(userID, authority))
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_7'
        elif checklist is True and checktrust is not True:
            return False, 'user_error_5'
        elif checklist is False:
            return False, 'user_error_7'
        else:
            return False, 'user_error'

    def MaskUser(self, USER):
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if (checklist is True and checktrust is True):
            self.conf.set('trustuser', USER, "{},0".format(userID))
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'user_success_2'
        else:
            return False, 'host_error_4'

    def UnmaskUser(self, USER, authority=5):
        if not ValueAuthority(authority):
            return False, 'user_error_9'
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if (checklist is True and checktrust is True):
            self.conf.set('trustuser', USER, "{},{}".format(userID, authority))
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_2'
        else:
            return False, 'host_error_4'

    def CheckUser(self, USER):
        checklist, userID = CheckUserExistAndGetID(
            self.conf, self.filepath, USER)
        checktrust = CheckUserExist(self.conf, self.filepath, USER)
        if checklist is True and checktrust is True:
            keyvalue = self.conf.get('trustuser', USER).split(',')
            return True, "{}=> userID:{} authority:{}".format(
                USER, keyvalue[0], keyvalue[1])
        else:
            return False, 'host_error_4'

    def ListAllUser(self):
        for item in self.conf.items('trusthost'):
            keyvalue = item[1].split(',')
            print("User: {}, UserID: {}, Authority: {}".format(
                item[0], keyvalue[0], keyvalue[1]))


def UserCommand(command):
    commandList = command.split(' ')
    userconfig = UserCommandConf()
    if commandList[1] is 'add':
        userconfig.UserListUpdate()
        return userconfig.AddUser(commandList[2], commandList[3])
    elif commandList[1] is 'remove':
        return userconfig.RemoveUser(commandList[2])
    elif commandList[1] is 'update':
        return userconfig.ChageUser(commandList[2], commandList[3])
    elif commandList[1] is 'mask':
        return userconfig.MaskUser(commandList[2])
    elif commandList[1] is 'unmask':
        return userconfig.UnmaskUser(commandList[2], commandList[3])
    else:
        return userconfig.ListAllHost()


# Test class
def main():
    filename = 'test_trust.conf'
    USER = '140.115.31.245'
    hostconfig = UserCommandConf(filename)
    print(hostconfig.AddUser(USER, 1))
    print(hostconfig.ListAllUser())
    print(hostconfig.RemoveUser(USER))
    print(hostconfig.AddUser(USER, 1))
    print(hostconfig.MaskUser(USER))
    print(hostconfig.CheckUser(USER))
    print(hostconfig.ListAllUser())
    print(hostconfig.UnmaskUser(USER, 1))
    print(hostconfig.CheckUser(USER))
    print(hostconfig.ListAllUser())


if __name__ == '__main__':
    main()
