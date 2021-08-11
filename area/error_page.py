#  Nikulin Vasily © 2021
from flask import render_template
from flask_mobility.decorators import mobile_template

from area import area


@area.app_errorhandler(400)
@area.app_errorhandler(401)
@area.app_errorhandler(403)
@area.app_errorhandler(404)
@area.app_errorhandler(408)
@area.app_errorhandler(415)
@area.app_errorhandler(500)
@mobile_template('area/{mobile/}error-page.html')
def error_page(error, template: str):
    messages = {
        400: ['Некорректный запрос',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
        401: ['Вы не вошли в систему',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        403: ['Ошибка при авторизации в ЭПОС.Школа',
              'Попробуйте ещё раз. При повторном возникновении ошибки проверьте пароль от '
              'ЭПОС.Школа и обновите его в профиле'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса'],
        408: ['Превышено время ожидания',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
        415: ['Неподдерживаемый формат файла',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
        500: ['Ошибка на стороне сайта',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку'],
    }

    return render_template(template,
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])
