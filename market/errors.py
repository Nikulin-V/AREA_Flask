from flask import request, render_template

from area.error_page import global_messages
from market import market

messages = {
    403: ['Нет прав доступа',
          'Управление пользователями доступно только администратору.<br>'
          'Управление фондовой биржей доступно только её создателю.'],
}


@market.route("/error")
def error_page():
    code = request.args.get("code")

    if code is None:
        code = 404
    else:
        code = int(code)

    if code in messages.keys():
        return render_template('market/error_page.html',
                               code=code,
                               title=messages[code][0],
                               message=messages[code][1]), code
    elif code in global_messages:
        return render_template('market/error_page.html',
                               code=code,
                               title=global_messages[code][0],
                               message=global_messages[code][1]), code
    else:
        return render_template('market/error_page.html',
                               code=404,
                               title=global_messages[404][0],
                               message=global_messages[404][1]), 404
