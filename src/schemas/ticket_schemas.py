from datetime import datetime
from pydantic import BaseModel
from src.schemas.user_schemas import UserPublic

class PostTicketRequest(BaseModel):
    title: str
    content: str

class TicketPublic(BaseModel):
    id: str
    title: str
    content: str
    resolved: bool
    creation_datetime: datetime
    author: UserPublic

    class Config:
        from_attributes = True