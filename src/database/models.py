from src.database.core import base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from datetime import datetime, timezone, timedelta
from uuid import uuid4

class Ticket(base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    content = Column(String)
    resolved = Column(Boolean, default=False)
    author = Column(Integer, ForeignKey("users.id"))
    creation_datetime = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    session = relationship("AuthSession", backref="user")
    is_admin = Column(Boolean, nullable=False, default=False)

class AuthSession(base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))

base.metadata.create_all(bind=engine)