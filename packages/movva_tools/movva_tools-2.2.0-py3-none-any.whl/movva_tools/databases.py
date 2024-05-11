from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
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
        _password, _db_name,
        is_async=False
    ) -> None:

        self.engine = None
        self.session = None
        self.is_async = is_async

        self._database_url = self._set_database_url(
            user=_user,
            db_name=_db_name,
            password=_password,
            host=_host,
            port=_port
        )

    def _set_database_url(self, user, password, host, port, db_name):
        _encoded_password = quote_plus(password)
        if self.is_async:
            return f"postgresql+asyncpg://{user}:{_encoded_password}@{host}:{port}/{db_name}"  # noqa
        else:
            return f"postgresql://{user}:{_encoded_password}@{host}:{port}/{db_name}"

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

        if not self.is_async:
            Session = sessionmaker(bind=self.engine)
        else:
            Session = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

        self.session = Session()

    @abstractmethod
    def connect(self):
        raise NotImplementedError


class RapidProDatabase(BaseRapidProDatabase):

    def connect(self):
        self._database_url = self.set_connection_isolation_level(
            read_only=False, database_url=self._database_url
        )
        if not self.is_async:
            self.engine = create_engine(self._database_url)
        else:
            self.engine = create_async_engine(self._database_url, echo=self.is_async)


class RapidProReadOnlyDatabase(BaseRapidProDatabase):

    def connect(self):
        self.__database_url = self.set_connection_isolation_level(
            read_only=True, database_url=self.__database_url
        )

        self.engine = create_engine(self.__database_url)
