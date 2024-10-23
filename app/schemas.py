from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponce(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post : PostResponce
    votes : int
    
    class Config:
        from_attributes = True
class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserOut(BaseModel):
    id : int
    email : EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str


#token response schema
class TokenResponce(BaseModel):
    access_token : str
    token_type : str

# data which are embeded with token shcema
class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1) # type: ignore