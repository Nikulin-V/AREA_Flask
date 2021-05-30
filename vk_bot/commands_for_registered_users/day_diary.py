from flask import abort
from PIL import Image, ImageDraw, ImageFont
from vk_api import VkApi
from vk_api.upload import VkUpload
from datetime import datetime

from vk_bot import command_system

from vk_bot.credentials import TOKEN
from data import epos, db_session
from data.vk_users import VkUser


epos = epos.EPOS()


def day_diary():
    """функция для формирования сегодняшнего дневника"""
    im = Image.new('RGB', (1920, 200), color='#CCEEFF')

    font = ImageFont.truetype("arial.ttf", 14)
    x = 10
    y = 10
    draw = ImageDraw.Draw(im)

    db_sess = db_session.create_session()

    user_vk_id = day_diary_command.id

    login = db_sess.query(VkUser.epos_login).filter(VkUser.vk_id == user_vk_id).first()[0]
    password = db_sess.query(VkUser.epos_password).filter(VkUser.vk_id == user_vk_id).first()[0]

    epos.run(login, password)
    response = epos.get_schedule()

    if response == 'timeout':
        abort(408)
        return 'Сайт ЭПОС.Школа не отвечает. Пожалуйста, повторите запрос.'

    current_date = datetime.now().day

    flag = False
    for day in response.keys():  # создание картинки с данными
        if day.split(', ')[0] == str(current_date):
            if response[day]['lessons']:
                for lesson_id in range(len(response[day]['lessons'])):
                    message = response[day]['lessons'][lesson_id].split(' ')
                    if message[0] == 'Алгебра':
                        flag = True
                        draw.text((x, y), ' '.join(message[:3]), font=font, fill='#1C0606')
                        draw.text((x, y + 18), ' '.join(message[3:]), font=font, fill='#1C0606')
                    elif len(message) > 2:
                        flag = True
                        draw.text((x, y), ' '.join(message[:2]), font=font, fill='#1C0606')
                        draw.text((x, y + 18), ' '.join(message[2:]), font=font, fill='#1C0606')
                    else:
                        draw.text((x, y), ' '.join(message), font=font, fill='#1C0606')
                    if response[day]['homeworks'][lesson_id]:
                        message = response[day]['homeworks'][lesson_id].split(' ')
                        if len(message) > 33:
                            draw.text((x + 180, y), ' '.join(message[:34]),
                                      font=font, fill='#1C0606')
                            y += 18
                            draw.text((x + 180, y), ' '.join(message[34:]),
                                      font=font, fill='#1C0606')
                        else:
                            draw.text((x + 180, y), ' '.join(message), font=font, fill='#1C0606')
                    if flag:
                        y += 36
                        flag = False
                    else:
                        y += 20
            else:
                draw.text((x, y), 'На сегодня нет расписания', font=font, fill='#1C0606')

    im.save('photo.jpg')

    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()

    response = VkUpload(vk).photo_messages('photo.jpg')[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

    message = ''
    return message, attachment


day_diary_command = command_system.Command()

day_diary_command.keys = ['дневник на сегодня']
day_diary_command.description = 'отправлю фото дневника на сегодняшний день'
day_diary_command.process = day_diary
