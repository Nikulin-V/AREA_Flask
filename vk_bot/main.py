import json

import message_handler

from flask import Flask, request

from credentials import TOKEN, confirmation_token
from data import db_session
from data.vk_users import VkUser


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/database.sqlite')
db_sess = db_session.create_session()


def main():
    app.run()


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if data['type'] == 'message_new':
        user: VkUser
        user = db_sess.query(VkUser).\
            filter(VkUser.vk_id == data['object']['message']['from_id']).first()
        last_message = db_sess.query(VkUser.last_message_id).\
            filter(VkUser.vk_id == data['object']['message']['from_id']).first()
        if user:

            """проверка id последнего сообщения (для устранения повторных запросов)"""

            if data['object']['message']['conversation_message_id'] > int(last_message[0]):

                """разделение сообщений по классам
                (для зарегистрированных пользователей ВК и незарегистрированных)"""

                if db_sess.query(VkUser.AREA_email).\
                        filter(VkUser.vk_id == data['object']['message']['from_id']).first():

                    """добавление id последнего сообщения (для устранения повторных запросов)"""
                    vk_user = db_sess.query(VkUser).\
                        filter(VkUser.vk_id == data['object']['message']['from_id']).first()
                    vk_user.last_message_id = data['object']['message']['conversation_message_id']
                    db_sess.commit()

                    message_handler.create_answer(True, data['object']['message'], TOKEN)
                    return 'ok', 200
                else:
                    message_handler.create_answer(False, data['object']['message'], TOKEN)
                    return 'ok', 200
            else:
                return 'ok', 200
        else:
            message_handler.create_answer(False, data['object']['message'], TOKEN)
            return 'ok', 200

    if 'type' not in data.keys():
        """обработка иных запросов"""
        return 'not vk', 500

    if data['type'] == 'confirmation':
        """обработка подтверждения для работы Callback API"""
        return confirmation_token, 200


if __name__ == '__main__':
    main()
