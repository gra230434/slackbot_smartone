import os


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
