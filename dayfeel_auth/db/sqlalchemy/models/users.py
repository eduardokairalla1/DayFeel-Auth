"""
Users model.
"""

# --- IMPORTS ---
from dayfeel_auth.db.sqlalchemy.setup.base import BASE
from dayfeel_auth.enums.user_role import UserRole
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship


# --- CODE ---
class Users(BASE):
    """
    Defines the user entity.
    """
    __tablename__ = 'users'
    __table_args__ = {'schema': 'auth'}

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(Enum(UserRole, name='user_role_enum', schema='auth'), nullable=False, default=UserRole.USER)
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=E1102
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # pylint: disable=E1102

    # ORM relationship
    sessions = relationship("AuthSessions", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
