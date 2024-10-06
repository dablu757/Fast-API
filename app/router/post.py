from fastapi import status,HTTPException,Depends, APIRouter
# from app import schemas,models
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from . import oauth2
# from oauth2 import get_current_user


router = APIRouter(
    prefix="/post"
)

#crete post path operation end-point
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_post(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user_id: models.User = Depends(oauth2.get_current_user)):
    
    if not current_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    print(f"current user : {current_user_id}")
    print(f"current user id : {current_user_id.id}")
    new_post = models.Post(owner_id=current_user_id.id, **post.model_dump())  # Use the user_id extracted from the token
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get post path operation end-point
@router.get("/", response_model=List[schemas.PostResponce])
def get_post(db : Session = Depends(get_db),current_user_id: models.User = Depends(oauth2.get_current_user)):
    _posts = db.query(models.Post).all()
    return _posts

#get post by id end-point
@router.get('/{id}', response_model=schemas.PostResponce)
def get_post_by_id(id : int, db : Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    return post

#delete post by id end-point
@router.delete('/{id}')
def post_deletion(id : int,
                  db : Session = Depends(get_db),
                  current_user : models.User = Depends(oauth2.get_current_user)):
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
@router.put('/{id}')
def post_update(id : int ,
                 update_post : schemas.PostBase, 
                 db : Session = Depends(get_db),
                 current_user : models.User=Depends(oauth2.get_current_user)):
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