#  Nikulin Vasily © 2021
from flask import render_template, redirect, request

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
    400: ['Некорректный запрос',
          'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
          'техподдержку'],
    401: ['Вы не вошли в систему',
          'Через несколько секунд Вы будете направлены на страницу авторизации'],
    403: ['Доступ запрещён',
          'Данный ресурс недоступен для вашего типа учетной записи'],
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
