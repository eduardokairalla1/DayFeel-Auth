"""
Auth sessions model.
"""

# --- IMPORTS ---
from dayfeel_auth.db.sqlalchemy.setup.base import BASE
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship


# --- CODE ---
class AuthSessions(BASE):
    """
    Defines the authentication sessions entity.
    """
    __tablename__ = 'auth_sessions'
    __table_args__ = {'schema': 'auth'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("auth.users.id", ondelete="CASCADE"), nullable=False, index=True)
    jti = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=E1102

    # ORM relationship
    user = relationship("Users", back_populates="sessions")
