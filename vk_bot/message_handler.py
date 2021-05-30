import importlib
import os
import vkapi

from data.users import User
from data.vk_users import VkUser
from data import db_session
from command_system import command_list


def get_answer(body, vk_id):
    """функция для получения ответного сообщения"""
    message = 'Простите, я не понимаю вас. Напишите "помощь", чтобы узнать мои команды.'
    attachment = ''
    for c in command_list:
        if body in c.keys:
            c.id = vk_id
            message, attachment = c.process()
    return message, attachment


def create_answer(is_registered, data, token):
    """функция для обработки полученных данных и их последующей отправки"""
    if not is_registered:
        if data['text'].startswith('/данные'):
            state_string = register(data)
            vkapi.send_message(data['from_id'], token, state_string)
        else:
            load_modules(is_registered)
            user_id = data['from_id']
            message, attachment = get_answer(data['text'].lower(), data['from_id'])
            vkapi.send_message(user_id, token, message, attachment)
    else:
        load_modules(is_registered)
        user_id = data['from_id']
        message, attachment = get_answer(data['text'].lower(), data['from_id'])
        vkapi.send_message(user_id, token, message, attachment)


def load_modules(is_registered):
    """функция для импортирования файлов с ответными сообщениями"""
    if is_registered:
        files = os.listdir("vk_bot/commands_for_registered_users")
        modules = filter(lambda x: x.endswith('.py'), files)
        for m in modules:
            importlib.import_module("commands_for_registered_users." + m[0:-3])
    else:
        files = os.listdir("vk_bot/commands_for_not_registered_users")
        modules = filter(lambda x: x.endswith('.py'), files)
        for m in modules:
            importlib.import_module("commands_for_not_registered_users." + m[0:-3])


def register(data):
    """функция для регистрации пользователя вк в системе (для занесения данных пользователя в БД)"""
    if len(data['text'].split()) == 3:
        area_login = data['text'].split()[1]
        area_password = data['text'].split()[2]
        vk_user_id = data['from_id']
        last_message = data['conversation_message_id']
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == area_login).first()
        if user and user.check_password(area_password):
            login_epos = db_sess.query(User.epos_login).filter(User.email == area_login).first()[0]
            password_epos = db_sess.query(User.epos_password).filter(
                User.email == area_login).first()[0]
            # noinspection PyArgumentList
            vk_user = VkUser(
                vk_id=vk_user_id,
                AREA_email=area_login,
                epos_login=login_epos,
                epos_password=password_epos,
                last_message_id=last_message
            )
            vk_user.set_password(area_password)
            db_sess.add(vk_user)
            db_sess.commit()
            return 'Вы успешно зарегистрировались.'
        else:
            return 'Неправильный email или пароль.'
    else:
        return 'Я не могу понять ваш запрос. Пожалуйста, повторите его.'
