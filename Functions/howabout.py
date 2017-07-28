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


def islivecommand(command):
    commandList = command.split(' ')
    if len(commandList) > 1:
        if islive(commandList[1]):
            return "{} is alive".format(commandList[1])
        else:
            return "ERROR: {} is not alive".format(commandList[1])
    else:
        if islivetogoogle():
            return "We can connect with 8.8.8.8"
        else:
            return "ERROR: We cannot connect 8.8.8.8"
