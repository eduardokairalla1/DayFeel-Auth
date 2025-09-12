"""
Database Connection Handler.
"""

# --- IMPORTS ---
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker


# --- TYPES ---
from types import TracebackType
from typing import Optional
from typing import Type


# --- CODE ---
class DbConnectionHandler:
    """
    Handler for database connection using SQLAlchemy.
    """

    def __init__(self, engine: Engine) -> None:
        """
        Initializes the handler.

        self.__engine: The SQLAlchemy engine instance.
        self.__session: Holds the current active session object.
        """
        self.__engine = engine
        self.__session = None


# --- Context management methods ---
    def __enter__(self) -> 'DbConnectionHandler':
        """
        Enters the context of the handler, opening a new session.

        :returns: The handler itself, with an active session.

        Usage:
            with DbConnectionHandler(engine) as db:
                # db.session can now be used
        """
        session_maker = self.__create_session_maker()
        self.__session = session_maker()
        return self


    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],  # pylint: disable=C0103
        exc_tb: Optional[TracebackType]  # pylint: disable=C0103
    ) -> None:
        """
        Exits the class context, closing the opened session.

        If an exception occurs, it rolls back the session and then closes it.
        If no exception occurs, it simply closes the session.

        :param exc_type: Type of the exception raised, if any.
        :param exc_val: Value of the exception raised, if any.
        :param exc_tb: Traceback object of the exception raised, if any.
        """
        try:
            if exc_type is not None:
                self.session.rollback()
        finally:
            self.session.close()


# --- Public properties ---
    @property
    def session(self) -> Session:
        """
        Returns the current active session.

        :raises RuntimeError: If the session has not been opened.
        """
        if self.__session is None:
            raise RuntimeError('Session is not open.')
        return self.__session


# --- Private helpers ---
    def __create_session_maker(self) -> sessionmaker:
        """
        Creates and returns a sessionmaker instance.

        :returns:  Configured sessionmaker.
        """
        return sessionmaker(
            bind=self.__engine,
            class_=Session,
            expire_on_commit=False,
        )
