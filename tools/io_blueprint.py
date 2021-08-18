#  Nikulin Vasily © 2021
from flask_socketio import emit

data_changes_functions = ['createCompany', 'deleteCompany',
                          'createNews', 'editNews', 'deleteNews',
                          'createOffer', 'editOffer', 'deleteOffer',
                          'createSession', 'editSession', 'deleteSession',
                          'createStockholdersVoting', 'voteInStockholdersVoting',
                          'createUser', 'editUser', 'deleteUser',
                          'voteInCompaniesVoting',
                          'investWallet']


class IOBlueprint:

    def __init__(self, namespace=None):
        self.namespace = namespace or '/'
        self._handlers = []

    def on(self, key):
        """ A decorator to add a handler to a blueprint. """

        def wrapper(f):
            if not callable(f):
                raise ValueError('handle must wrap a callable')

            def wrap(io):
                @io.on(key, namespace=self.namespace)
                def wrapped(*args, **kwargs):
                    from app import scheduler
                    if not scheduler.works:
                        scheduler.run()
                    if f.__name__ in data_changes_functions:
                        emit('renderPage', broadcast=True)
                    return f(*args, **kwargs)

                return io

            self._handlers.append(wrap)

        return wrapper

    def init_io(self, io):
        for f in self._handlers:
            f(io)

        return io
