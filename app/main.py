import sys
sys.path.append('')
from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
from database import engine,get_db

models.Base.metadata.create_all(bind=engine) #create table in database

app=FastAPI()


#get metghod
@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post)
    print(posts)
    return {"data" : "success"}


@app.get("/posts")
def get_post(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts}


#get post by id
@app.get("/posts/{id}")
def get_post_by_id(id : int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    print(post)
    return {"post_detail" : post}

