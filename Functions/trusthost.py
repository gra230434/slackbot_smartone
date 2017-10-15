#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
import configparser


roles = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)\
{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def TrustHostExist(conf, filepath):
    conf.read(filepath)
    sections = conf.sections()
    if 'trusthost' in sections:
        return True
    else:
        return False


def CheckHostExist(conf, filepath, keyname):
    if TrustHostExist(conf, filepath):
        conf.read(filepath)
        if keyname in conf['trusthost']:
            return True
        else:
            return False
    else:
        return False


def CheckIsIP(HOST):
    """ Check IP or Domain
    return True is IP
    retunr False is Domain
    """
    if re.match(roles, HOST):
        return True
    else:
        return False


def ExtractHostname(HOST):
    if HOST.find("://") > -1:
        hostname = HOST.split('/')[2]
    else:
        hostname = HOST.split('/')[0]
    hostname = hostname.split(':')[0]
    hostname = hostname.split('?')[0]
    return hostname


def CreateKeyname(HOST):
    """
    IP input and return HOST_XXX_XXX_XXX_XXX
    140.115.31.245 return HOST_140_115_31_245
    blog.technologyofkevin.com return HOST_blog_technologyofkevin_com
    """
    if CheckIsIP(HOST):
        tmp = HOST.split(".")
        keyname = "HOST_{}_{}_{}_{}".format(tmp[0], tmp[1], tmp[2], tmp[3])
    else:
        hostname = ExtractHostname(HOST)
        tmp = hostname.replace(".", "_")
        keyname = "HOST_{}".format(tmp)
    return keyname


class HostCommandConf(object):
    """docstring for HostCommand"""
    def __init__(self, filename='trust.conf'):
        super(HostCommand, self).__init__()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.filepath = os.path.join(self.dirpath, filename)
        self.conf = configparser.ConfigParser()
        readconfig = self.ReadConf()
        if readconfig[0] is not True:
            return readconfig[1]

    def ReadConf(self):
        if os.path.isfile(self.filepath):
            if TrustHostExist(self.conf, self.filepath):
                return True, 'success'
            else:
                return False, 'host_error_2'
        else:
            return False, 'host_error_1'

    def AddHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if not CheckHostExist(self.conf, self.filepath, keyname):
            self.conf.set('trusthost', keyname, 'true')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_1'
        else:
            keyvalue = self.conf.getboolean('trusthost', keyname)
            if keyvalue is False:
                if self.UnmaskHost(HOST)[0] is True:
                    return True, 'host_success_2'
                else:
                    return False, 'host_error_4'
            return False, 'host_error_3'

    def RemoveHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, self.filepath, keyname):
            self.conf.remove_option('trusthost', keyname)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_3'
        else:
            return False, 'host_error_4'

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
    hostconfig = HostCommandConf()
    if commandList[1] is 'add':
        return hostconfig.AddHost(commandList[2])
    elif commandList[1] is 'remove':
        return hostconfig.RemoveHost(commandList[2])
    elif commandList[1] is 'mask':
        return hostconfig.MaskHost(commandList[2])
    elif commandList[1] is 'unmask':
        return hostconfig.UnmaskHost(commandList[2])
    else:
        return hostconfig.ListAllHost()


# Test class
def main():
    filename = 'test_trust.conf'
    IPhost = '140.115.31.245'
    Domainhost = 'blog.technologyofkevin.com'
    hostconfig = HostCommandConf(filename)
    print(hostconfig.AddHost(IPhost))
    print(hostconfig.AddHost(Domainhost))
    print(hostconfig.ListAllHost())
    print(hostconfig.RemoveHost(IPhost))
    print(hostconfig.MaskHost(Domainhost))
    print(hostconfig.CheckHost(Domainhost))
    print(hostconfig.ListAllHost())
    print(hostconfig.UnmaskHost(Domainhost))
    print(hostconfig.CheckHost(Domainhost))
    print(hostconfig.ListAllHost())


if __name__ == '__main__':
    main()
