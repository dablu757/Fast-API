from fastapi import FastAPI
import models
from database import engine
from router import post, user


models.Base.metadata.create_all(bind=engine) #create table in database

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)