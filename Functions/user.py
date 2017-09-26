import re
import os
import configparser


def TrustUserExist(conf, filepath):
    conf.read(filepath)
    sections = conf.sections()
    if 'trusthost' in sections:
        return True
    else:
        return False


def CheckUserExist(conf, filepath, keyname):
    if TrustUserExist(conf, filepath):
        conf.read(filepath)
        if keyname in conf['trusthost']:
            return True
        else:
            return False
    else:
        return False


def main():
    pass


if __name__ == '__main__':
    main()
