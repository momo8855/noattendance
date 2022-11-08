from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    course_name: str
    lecture_num: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Resp(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Resp
    attend_num: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None


class Vote(BaseModel):
    lec_id: int
    dir: conint(le=1)



class All(BaseModel):
    full_name: str
    course_name: str
    lecture_num: str

    class Config:
        orm_mode = True
    
    


    



