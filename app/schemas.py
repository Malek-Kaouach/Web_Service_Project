from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    location: Optional[str]=""
    location_link: Optional[str]= "MAPS LINK"
    #choosing a dummy variable in order to not get an empty input error
    #location_link will use the value of the location to transform it into google maps link
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


class AdminOut(BaseModel):
    id: int
    name: str
    location: str
    availability: Optional[str]
    response_radius: Optional[int]
    current_status: Optional[str]

    class config:
        orm_mode=True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    #owner_id: int
    #owner_phone_number: int
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


class AdminCreate(BaseModel):
    name: str
    password: str
    location: str
    availability: Optional[str] = "24/7"
    response_radius: Optional[int]= 50
    current_status: Optional[str]= 'unknown'



class UserLogin(BaseModel):
    phone_number: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None