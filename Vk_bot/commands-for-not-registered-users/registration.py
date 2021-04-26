import command_system


def registration():
    """функция для формирования регистрационного шаблона"""
    return 'введите свои учетные данные от сайта AREA в формате:\n' \
           '/данные <email> <пароль>', ''


reg_command = command_system.Command()

reg_command.keys = ['зарегистрироваться']
reg_command.description = 'зарегистрирую вас в системе'
reg_command.process = registration
