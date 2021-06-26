import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


# noinspection PyUnresolvedReferences
def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from .classes import Class
    from .companies import Company
    from .epos import EPOS
    from .groups import Group
    from .homeworks import Homework
    from .news import News
    from .offers import Offer
    from .schools import School
    from .sessions import Session
    from .stockholders_votes import SVote
    from .stocks import Stock
    from .students import Student
    from .transactions import Transaction
    from .users import User
    from .vk_users import VkUser
    from .votes import Vote
    from .wallets import Wallet

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    # noinspection PyCallingNonCallable
    return __factory()
