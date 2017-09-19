import re
import os
import configparser


roles = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)\
{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def TrustHostExist(filepath):
    conf = configparser.ConfigParser()
    conf.read(filepath)
    sections = conf.sections()
    if 'trusthost' in sections:
        return True
    else:
        return False


def CheckCanInsert(conf, filepath):
    if os.path.isfile(filepath):
        if TrustHostExist(conf, filepath):
            return True
        else:
            return False
    else:
        return False


def CheckIPorDomain(HOST):
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
    if CheckIPorDomain(HOST):
        tmp = HOST.split(".")
        keyname = "HOST_{}_{}".format(tmp[2], tmp[3])
    else:
        hostname = ExtractHostname(HOST)
        tmp = hostname.replace(".", "_")
        keyname = "HOST_{}".format(tmp)
    return keyname


class HostCommand(object):
    """docstring for HostCommand"""
    def __init__(self, arg):
        super(HostCommand, self).__init__()
        self.dirpath = os.path.dirname(os.path.realpath(__file__))
        self.filepath = os.path.join(self.dirpath, 'trust.conf')
        if not self.ReadConf():
            return False, 'error_1'

    def ReadConf(self):
        conf = configparser.ConfigParser()
        if os.path.isfile(self.filepath):
            conf = configparser.ConfigParser()
            self.conf = conf.read(self.filepath)
            return True
        else:
            return False

    def AddHost(self, HOST):
        if CheckCanInsert(self.conf, self.filepath):
            keyname = CreateKeyname(HOST)
            pass

    def RemoveHost():
        pass

    def CheckHost():
        pass


def main():
    pass
