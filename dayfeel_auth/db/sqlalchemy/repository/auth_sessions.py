"""
AuthSessions table repository.
"""

# --- IMPORTS ---
from datetime import datetime
from datetime import timezone
from dayfeel_auth.db.sqlalchemy.models.auth_sessions import AuthSessions
from dayfeel_auth.db.sqlalchemy.setup.db_connection_handler import DbConnectionHandler
from dayfeel_auth.err.database_unavailable_error import DatabaseUnavailableError
from sqlalchemy import Engine


# --- TYPES ---
from typing import Optional


# --- CODE ---
class AuthSessionsRepository:
    """
    Repository responsible for operations related to the auth_sessions table.
    """

    def __init__(self, engine: Engine) -> None:
        """
        Initializes the storage.

        :param engine: SQLAlchemy engine.

        :returns: None.
        """
        self.__engine = engine


    def insert_session(self, session: AuthSessions) -> AuthSessions:
        """
        Insert a new authentication session to database.

        :param session: New authentication session.

        :returns: Persisted authentication session with updated fields.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Insert session into database
                db.session.add(session)

                # Commit changes
                db.session.commit()

                # Refresh session instance
                db.session.refresh(session)

                # Return new inserted session
                return session

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def get_by_jti(self, jti: str) -> Optional[AuthSessions]:
        """
        Retrieve a session by its JWT "jti".

        :param jti: Unique JWT identifier.

        :returns: AuthSessions or None if not found.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Retrieve session by jti from database
                query = db.session.query(AuthSessions).filter(AuthSessions.jti == jti).one_or_none()

                # Return AuthSessions or None
                return query

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def revoke_session(self, jti: str) -> None:
        """
        Revoke a session.

        :param jti: Unique JWT identifier.

        :returns: None.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Retrieve session by jti from database
                session = db.session.query(AuthSessions).filter(AuthSessions.jti == jti).one_or_none()

                # If session exists: revoke session
                if session:

                    # Set revoked field = True
                    session.revoked = True

                    # Commit changes
                    db.session.commit()

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e


    def delete_expired_sessions(self) -> int:
        """
        Delete all expired sessions to clean up the table.

        :returns: Number of deleted rows.
        """
        # Open database connection
        with DbConnectionHandler(self.__engine) as db:
            try:
                # Current datetime (UTC)
                now = datetime.now(timezone.utc)

                # Delete all sessions where expires_at < now
                result = db.session.query(AuthSessions).filter(AuthSessions.expires_at < now).delete()

                # Commit changes
                db.session.commit()

                # Return number of deleted rows
                return result

            # If database is unavailable: raise error
            except Exception as e:
                raise DatabaseUnavailableError(e) from e
