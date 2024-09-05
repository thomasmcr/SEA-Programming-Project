from src.database.core import base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4

from src.schemas.ticket_schemas import TicketPublic
from src.schemas.user_schemas import UserPublic

class Ticket(base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    content = Column(String)
    resolved = Column(Boolean, default=False)
    creation_datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    comments = relationship("Comment", back_populates="ticket")
    author = relationship("User")
    author_id = Column(Integer, ForeignKey("users.id"))

    def get_ticket_public(self):
        return TicketPublic.model_validate(self)

class Comment(base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    content = Column(String)
    ticket_id = Column(String, ForeignKey("tickets.id"))
    ticket = relationship("Ticket", back_populates="comments")

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    session = relationship("AuthSession", backref="user")
    is_admin = Column(Boolean, nullable=False, default=False)

    def get_user_public(self):
        return UserPublic.model_validate(self)

class AuthSession(base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))

base.metadata.create_all(bind=engine)