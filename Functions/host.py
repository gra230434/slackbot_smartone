import re
import os
import configparser


roles = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.)\
{3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"


def TrusthostExist(filepath):
    conf = configparser.ConfigParser()
    conf.read(filepath)
    sections = conf.sections()
    if trusthost in sections:
        return True
    else:
        return False


def ConfigExist(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def CheckCanInsert(filepath):
    if ConfigExist(filepath):
        if TrusthostExist(filepath):
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


def CreateKeyname(HOST):
    if CheckIPorDomain(HOST):
        tmp = HOST.split(".")
        KEYNAME = "HOST_{}_{}".format(tmp[2], tmp[3])
    else:
        tmp = HOST.replace(".", "_")
        KEYNAME = "HOST_{}".format(tmp)
    return KEYNAME


def add_Host(HOST):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, 'trust.conf')
    if CheckCanInsert(filepath):
        KEYNAME = CreateKeyname(HOST)
        pass


def main():
    pass
