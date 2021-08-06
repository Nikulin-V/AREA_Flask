#  Kozhevnikov Kirill © 2021

import vk

session = vk.Session()
api = vk.API(session, v='5.130')


# noinspection PyUnusedLocal
def send_message(user_id, token, message, attachment=""):
    """функция для отправки сообщений"""
    api.messages.send()
