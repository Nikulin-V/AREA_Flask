command_list = []


class Command:
    """класс команд (ответных сообщений)"""
    def __init__(self):
        self.__keys = []  # список команд (ответных сообщений)
        self.description = ''  # описание команд (ответных сообщений)
        self.__id = 0  # id пользователя ВК (для передачи внутрь файлов с командами)
        command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, vk_id):
        self.__id = vk_id

    def process(self):
        """функция для формирования ответного сообщения"""
        pass
