from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from src.schemas.user_schemas import UserPublic

class PostTicketRequest(BaseModel):
    title: str
    content: str
    
class UpdateTicketRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostCommentRequest(BaseModel):
    content: str    

class CommentPublic(BaseModel):
    id: str
    content: str
    ticket_id: str
    author: UserPublic
    creation_datetime: datetime
    class Config:
        from_attributes = True

class TicketPublic(BaseModel):
    id: str
    title: str
    content: str
    resolved: bool
    creation_datetime: datetime
    author: UserPublic
    comments: List[CommentPublic]

    class Config:
        from_attributes = True