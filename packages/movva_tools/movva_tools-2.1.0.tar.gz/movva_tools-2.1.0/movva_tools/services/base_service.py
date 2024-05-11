from movva_tools.databases import RapidProDatabase
from sqlalchemy.exc import SQLAlchemyError


class BaseService:

    def __init__(
        self,
        _user=None, _host=None, _port=None, _db_name=None, _password=None,
        db_connection=None
    ) -> None:
        if not db_connection:
            self.db_connection = self.__create_default_connection(
                _user=_user,
                _password=_password,
                _host=_host,
                _port=_port,
                _db_name=_db_name
            )
        else:
            self.db_connection = db_connection

    def __create_default_connection(self, _user, _host, _port, _db_name, _password):  # noqa
        db = RapidProDatabase(
            _user=_user,
            _password=_password,
            _host=_host,
            _port=_port,
            _db_name=_db_name
        )
        db.set_session()
        return db

    def add(self, object):
        self.db_connection.session.add(object)

    def commit(self):
        self.db_connection.session.commit()

    def flush(self):
        """
            Flush para obter o ID gerado sem commit
        """
        self.db_connection.session.flush()

    def rollback_session(self):
        try:
            self.db_connection.session.rollback()
            return True
        except SQLAlchemyError as e:
            raise Exception(e)

    def close_session(self):
        self.db_connection.session.close()
