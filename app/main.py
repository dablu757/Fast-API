from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
import models
from database import engine,get_db
import schemas
from typing import List

models.Base.metadata.create_all(bind=engine) #create table in database

app=FastAPI()

#crete post path operation end-point
@app.post("/post", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_post(post : schemas.PostCreate , db : Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) #unpacked dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get post path operation end-point
@app.get("/get_post", response_model=List[schemas.PostResponce])
def get_post(db : Session = Depends(get_db)):
    _posts = db.query(models.Post).all()
    return _posts

#get post by id end-point
@app.get('/post/{id}', response_model=schemas.PostResponce)
def get_post_by_id(id : int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post

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

#update path operation
@app.put('/update/{id}')
def post_update(id : int , update_post : schemas.PostBase, db : Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} not found"
        )
    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()
    return {'status' : 'post updated successfully'}