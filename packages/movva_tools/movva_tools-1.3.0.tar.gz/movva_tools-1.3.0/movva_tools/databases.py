from abc import ABC, abstractmethod
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from movva_tools.constants import READ_ONLY_ISOLATION_LEVEL_CONNECTION


Base = declarative_base()


class BaseRapidProDatabase(ABC):

    def __init__(
        self,
        _user, _host, _port,
        _password, _db_name
    ) -> None:

        self.engine = None
        self.session = None

        _encoded_password = quote_plus(_password)
        self._database_url = f"postgresql://{_user}:{_encoded_password}@{_host}:{_port}/{_db_name}"  # noqa

    # def set_connection(
    #     self, password, user, host, port, db_name
    # ):
    #     try:
    #         encoded_password = quote_plus(password)
    #         user = user
    #         host = host
    #         port = port
    #         db_name = db_name

    #         self._database_url = f"postgresql://{user}:{encoded_password}@{host}:{port}/{db_name}" # noqa

    #     except Exception:
    #         raise ConnectionError(
    #             'As informações de conexão com o banco de dados não foram encontradas.' # noqa
    #         )

        # try:
        #     encoded_password = quote_plus(os.environ.get('DB_PASSWORD'))
        #     user = os.environ.get('DB_USER')
        #     host = os.environ.get('DB_HOST')
        #     port = os.environ.get('DB_PORT')
        #     db_name = os.environ.get('DB_NAME')
        #     self._database_url = f"postgresql://{user}:{encoded_password}@{host}:{port}/{db_name}" # noqa
        # except Exception:
        #     raise ConnectionError(
        #         'As informações de conexão com o banco de dados não foram encontradas.' # noqa
        #     )

    def set_connection_isolation_level(self, database_url: str, read_only=True) -> str:  # noqa
        if read_only:
            return database_url+READ_ONLY_ISOLATION_LEVEL_CONNECTION

        return database_url

    def execute_query(self, query, params=None):
        try:
            if not self.engine:
                self.connect()
            conn = self.engine.connect()

            if params is None:
                response = conn.execute(query)
            else:
                response = conn.execute(query, **params)

            conn.close()  # Certifique-se de fechar a conexão
            return response
        except Exception as e:
            conn.close()
            raise e

    def set_session(self):
        if not self.engine:
            self.connect()

        Session = sessionmaker(bind=self.engine)

        self.session = Session()

    @abstractmethod
    def connect(self):
        raise NotImplementedError


class RapidProDatabase(BaseRapidProDatabase):

    def connect(self):
        self._database_url = self.set_connection_isolation_level(
            read_only=False, database_url=self._database_url
        )

        self.engine = create_engine(self._database_url)


class RapidProReadOnlyDatabase(BaseRapidProDatabase):

    def connect(self):
        self.__database_url = self.set_connection_isolation_level(
            read_only=True, database_url=self.__database_url
        )

        self.engine = create_engine(self.__database_url)
