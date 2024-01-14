from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    location: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostStatus(BaseModel):
    published: bool = True


class UserOut(BaseModel):
    phone_number: str
    name: str
    age: Optional[int]
    home_location: str

    class config:
        orm_mode=True



class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner_phone_number: int
    status: str
    owner: UserOut
    
    class config:
        orm_mode=True


class UserCreate(BaseModel):
    phone_number: str
    password: str
    name: str
    age: Optional[int] = None
    home_location: str



class UserLogin(BaseModel):
    phone_number: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None