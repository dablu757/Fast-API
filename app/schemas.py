from pydantic import BaseModel, EmailStr
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponce(PostBase):
    id : int
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