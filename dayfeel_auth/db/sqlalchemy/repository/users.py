"""
Users table respository.
"""

# --- IMPORTS ---
from datetime import datetime
from datetime import timezone
from dayfeel_auth.db.sqlalchemy.models.users import Users
from dayfeel_auth.db.sqlalchemy.setup.db_connection_handler import DbConnectionHandler
from dayfeel_auth.err.already_exists_error import AlreadyExistsError
from dayfeel_auth.err.database_unavailable_error import DatabaseUnavailableError
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError


# --- TYPES ---
from typing import Optional


# --- CODE ---
class UsersRepository:
    """
    Repository responsible for operations related to the users table.
    """
    def __init__(self, engine: Engine) -> None:
        """
        Initializes the storage.

        :param engine: SQLAlchemy engine.

        :returns: None.
        """
        self.__engine = engine


    def insert_user(self, user: Users) -> Users:
        """
        Insert a new user to database.

        :param user: User model instance.

        :returns: Persisted user with updated fields.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Insert user to database
                db.session.add(user)

                # Commit changes
                db.session.commit()

                # Refresh user instance
                db.session.refresh(user)

                # Return new insert user
                return user

            # If the user already exists: raise error
            except IntegrityError as e:
                raise AlreadyExistsError({'entity': 'user',
                                          'local': 'database',
                                          'detail': e}) from e

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def get_by_email(self, email: str) -> Optional[Users]:
        """
        Retrieves a user by email.

        :param email: email associete with user.

        :returns: User or None if not found.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Retrieves user by email from database
                query = db.session.query(Users).filter(Users.email == email).one_or_none()

                # Returns User ou None
                return query

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def get_by_id(self, user_id: int) -> Optional[Users]:
        """
        Retrieves a user by id.

        :param user_id: Id associete by user.

        :returns: User or None if not found.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Retrieves user by id from database
                query = db.session.query(Users).filter(Users.id == user_id).one_or_none()

                # Returns User ou None
                return query

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def update_last_login(self, user_id: int) -> None:
        """
        Update the last_login field of a specific user.

        :param user_id: User's unique identificator.

        :returns: None.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Update last_login field of the user
                db.session.query(Users).filter(
                    Users.id == user_id
                ).update(
                    {Users.last_login: datetime.now(timezone.utc)},
                    synchronize_session=False
                )

                # Commit changes
                db.session.commit()

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e
