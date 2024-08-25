from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str 

class UserPublic(BaseModel):
    id: int
    username: str 
    class Config:
        orm_mode = True