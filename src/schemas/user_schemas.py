from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str 

class RegisterRequest(BaseModel):
    username: str
    password: str

class UserPublic(BaseModel):
    id: int
    username: str 
    is_admin: bool
    class Config:
        from_attributes = True