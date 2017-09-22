import re
import os
import configparser


roles = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)\
{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def TrustHostExist(conf):
    sections = conf.sections()
    if 'trusthost' in sections:
        return True
    else:
        return False


def CheckHostExist(conf, keyname):
    if TrustHostExist(conf):
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
        readconfig = self.ReadConf()
        if not readconfig[0]:
            return False, readconfig[1]

    def ReadConf(self):
        if os.path.isfile(self.filepath):
            conf = configparser.ConfigParser()
            self.conf = conf.read(self.filepath)
            if TrustHostExist(self.conf):
                return True
            else:
                return False, 'host_error_2'
        else:
            return False, 'host_error_2'

    def AddHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if not CheckHostExist(self.conf, keyname):
            self.conf.set('trusthost', keyname, 'true')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_1'
        else:
            return False, 'host_error_3'

    def RemoveHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, keyname):
            self.conf.remove_option('trusthost', keyname)
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_3'
        else:
            return False, 'host_error_4'

    def MaskHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, keyname):
            self.conf.set('trusthost', keyname, 'false')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_2'
        else:
            return False, 'host_error_4'

    def UnmaskHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, keyname):
            self.conf.set('trusthost', keyname, 'true')
            with open(self.filepath, 'w') as configfile:
                self.conf.write(configfile)
            return True, 'host_success_2'
        else:
            return False, 'host_error_4'

    def CheckHost(self, HOST):
        keyname = CreateKeyname(HOST)
        if CheckHostExist(self.conf, keyname):
            ksyvalue = self.conf.getboolean('trusthost', keyname)
            return True, "{}: key:{} value:{}".format(HOST, keyname, ksyvalue)
        else:
            return False, 'host_error_4'

    def ListAllHost(self, HOST):
        for item in self.conf.items('trusthost'):
            print "Host: {}, isMask: {}".format(item[0], item[1])


def main():
    pass


if __name__ == '__main__':
    main()
