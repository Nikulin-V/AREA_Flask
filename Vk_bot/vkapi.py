import vk
import random

session = vk.Session()
api = vk.API(session, v='5.130')


def send_message(user_id, token, message, attachment=""):
    """функция для отправки сообщений"""
    api.messages.send(access_token=token, user_id=str(user_id), message=message,
                      attachment=attachment, random_id=random.getrandbits(64))
