#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import configparser


def ReadHostConf(filename='trust.conf'):
    conf = configparser.ConfigParser()
    conf.read(filename)
    return conf.options('trusthost')


def HostCheckConf(host):
    hostlist = ReadHostConf()
    if host in hostlist:
        return True
    else:
        return False


def islivetogoogle():
    response = os.system("ping -c 1 8.8.8.8")
    if response == 0:
        return True
    else:
        return False


def islive(host):
    response = os.system("ping -c 1 {}".format(host))
    # and then check the response...
    if response == 0:
        return True
    else:
        return False


def islivecommand(command):
    commandList = command.split(' ')
    if len(commandList) > 1:
        if HostCheckConf(commandList[1]):
            if islive(commandList[1]):
                return "{} is alive".format(commandList[1])
            else:
                return "ERROR: {} is not alive".format(commandList[1])
        else:
            return "ERROR: {} is not in TrustHost".format(commandList[1])
    else:
        if islivetogoogle():
            return "We can connect with 8.8.8.8"
        else:
            return "ERROR: We cannot connect 8.8.8.8"
