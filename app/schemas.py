from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


class CreatePost(PostBase):
    pass


class Posts(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    created_at : datetime
    class Config:
        orm_mode = True #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
                        # but an ORM model (or any other arbitrary object with attributes).



class UserCreate(BaseModel):
    email : EmailStr
    password : str


class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    class Config:
        orm_mode = True