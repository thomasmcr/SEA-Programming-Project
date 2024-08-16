from src.database.core import base, engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship 
from datetime import datetime, timedelta
from uuid import uuid4

class Ticket(base):
    __tablename__ = "tickets"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String)
    content = Column(String)
    resolved = Column(Boolean, default=False)

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    session = relationship("AuthSession", backref="user")

class AuthSession(base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    expiry_datetime = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30))
    user_id = Column(Integer, ForeignKey("users.id"))

base.metadata.create_all(bind=engine)