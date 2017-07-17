def repeatcommand(command):
    if command.find(' ') != -1:
        return 'Hi Sir, repeat'
    else:
        code = command.split(' ')
    recommand = code[1]
    for val in code[2:]:
        recommand = "{} {}".format(recommand, val)
    return recommand
