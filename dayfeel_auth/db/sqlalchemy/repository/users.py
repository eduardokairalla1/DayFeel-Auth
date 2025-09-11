"""
Users table respository.
"""

# --- IMPORTS ---
from dayfeel_auth.db.sqlalchemy.models.users import Users
from dayfeel_auth.db.sqlalchemy.setup.db_connection_handler import DbConnectionHandler
from dayfeel_auth.err.already_exists_error import AlreadyExistsError
from dayfeel_auth.err.database_unavailable_error import DatabaseUnavailableError
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError


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
