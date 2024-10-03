from pydantic import BaseModel

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponce(BaseModel):
    title : str
    content : str
    published : bool
    id : int
    class Config:
        orm_mode = True