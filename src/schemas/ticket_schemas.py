from fastapi import Cookie
from pydantic import BaseModel

class PostTicketRequest(BaseModel):
    title: str
    content: str