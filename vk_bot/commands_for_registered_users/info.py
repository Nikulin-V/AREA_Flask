import command_system


def info():
    """функция для формирования списка с командами"""
    message = ''
    for c in command_system.command_list:
        message += c.keys[0] + ' - ' + c.description + '\n'
    return message, ''


info_command = command_system.Command()

info_command.keys = ['помощь']
info_command.description = 'покажу список команд'
info_command.process = info
