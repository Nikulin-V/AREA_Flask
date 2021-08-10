#  Nikulin Vasily © 2021
from flask import Blueprint
from tools.io_blueprint import IOBlueprint

api = Blueprint('api', __name__)
sock = IOBlueprint()

# noinspection PyPep8
from .companies import createCompany, getCompanies, deleteCompany
from .news import createNews, getNews, editNews, deleteNews
from .offers import createOffer, getOffers, editOffer, deleteOffer
from .sessions import createSession, getSessions, editSession, deleteSession
from .stocks import getStocks
from .svotes import createStockholdersVoting, getStockholdersVotes, voteInStockholdersVoting
from .users import createUser, getUsers, editUser, deleteUser
from .votes import getCompaniesVotes, voteInCompaniesVoting
from .wallets import getWallet
