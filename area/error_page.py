#  Nikulin Vasily © 2021
from flask import render_template, redirect, request
from flask_babel import _

from area import area
from tools.url import url


@area.app_errorhandler(400)
@area.app_errorhandler(401)
@area.app_errorhandler(403)
@area.app_errorhandler(404)
@area.app_errorhandler(408)
@area.app_errorhandler(415)
@area.app_errorhandler(500)
def error_handler(error):
    if error.code == 404:
        return redirect(url(request.host.split(".")[0].split("-")[0] + ".error_page"))
    return redirect(url(".error_page") + f"?code={error.code}")


global_messages = {
    400: [_('Некорректный запрос'),
          _('Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
            'техподдержку')],
    401: [_('Вы не вошли в систему'),
          _('Через несколько секунд Вы будете направлены на страницу авторизации')],
    403: [_('Доступ запрещён'),
          _('Данный ресурс недоступен для вашего типа учетной записи')],
    404: [_('Страница не найдена'),
          _('Проверьте правильность введённого адреса')],
    408: [_('Превышено время ожидания'),
          _('Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
            'техподдержку')],
    415: [_('Неподдерживаемый формат файла'),
          _('Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
            'техподдержку')],
    500: [_('Ошибка на стороне сайта'),
          _('Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
            'техподдержку')],
}


@area.route("/error")
def error_page():
    code = request.args.get("code")

    if code is None:
        code = 404
    else:
        code = int(code)

    if code not in global_messages.keys():
        code = 404

    return render_template('area/error_page.html',
                           code=code,
                           title=global_messages[code][0],
                           message=global_messages[code][1]), code
