#  Nikulin Vasily © 2021
from flask_login import login_required, current_user

from data import db_session
from data.functions import get_session_id, get_company_title
from data.stocks import Stock
from market.api import api, socket
from tools.tools import send_response


@socket.on('getStocks')
@api.route('/api/stocks', methods=['GET'])
@login_required
def getStocks():
    """

    Returns: current stocks JSON

    """

    event_name = 'getStocks'

    db_sess = db_session.create_session()
    stocks = db_sess.query(Stock).filter(
        Stock.session_id == get_session_id(),
        Stock.user_id == current_user.id
    ).all()
    s: Stock

    return send_response(
        event_name,
        {
            'message': 'Success',
            'stocks':
                [
                    {
                        'id': s.id,
                        'company': get_company_title(s.company_id),
                        'stocks': s.stocks
                    }
                    for s in sorted(stocks, key=lambda x: get_company_title(x.company_id))]
        }
    )
