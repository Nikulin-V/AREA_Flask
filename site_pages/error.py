#  Nikulin Vasily (c) 2021
from flask import Blueprint, render_template
from flask_mobility.decorators import mobile_template

error_page = Blueprint('error', __name__)
app = error_page


@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(408)
@mobile_template('{mobile/}error-page.html')
def page_not_found(error, template):
    messages = {
        401: ['Вы не авторизованы',
              'Через несколько секунд Вы будете направлены на страницу авторизации'],
        403: ['Ошибка при авторизации в ЭПОС.Школа',
              'Попробуйте ещё раз. При повторном возникновении ошибки проверьте пароль от '
              'ЭПОС.Школа и обновите его в профиле'],
        404: ['Страница не найдена',
              'Проверьте правильность введённого адреса'],
        408: ['Превышено время ожидания',
              'Попробуйте сделать запрос еще раз. Если проблема повторится, обратитесь в '
              'техподдержку']
    }

    return render_template(template,
                           code=error.code,
                           title=messages[error.code][0],
                           message=messages[error.code][1])
