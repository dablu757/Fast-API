from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
import models
from database import engine,get_db
from schemas import *

models.Base.metadata.create_all(bind=engine) #create table in database

app=FastAPI()

#test path operation end-point
@app.get("/sqlalchemy")
def test_sqlalchemy(db : Session = Depends(get_db)):
    return {"status" : "success"}


#crete post path operation end-point
@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post : PostCreate , db : Session = Depends(get_db)):
    # new_post = models.Post(
    #     title = post.title,
    #     content = post.content
    # )

    new_post = models.Post(**post.model_dump()) #unpacked dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"data" : new_post}


#get post path operation end-point
@app.get("/get_post")
def get_post(db : Session = Depends(get_db)):
    _posts = db.query(models.Post).all()
    return {'posts' : _posts}

#get post by id end-point
@app.get('/post/{id}')
def get_post_by_id(id : int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return {"data" : post}


#delete post by id end-point
@app.delete('/delete_post/{id}')
def post_deletion(id : int, db : Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"post with id : {id} does not exist"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message' : f"post with id : {id} deleted successfully"}