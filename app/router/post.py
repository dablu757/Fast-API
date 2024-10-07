from fastapi import status,HTTPException,Depends, APIRouter
# from app import schemas,models
import schemas, models
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from . import oauth2
from typing import Optional
# from oauth2 import get_current_user


router = APIRouter(
    prefix="/post"
)

#crete post path operation end-point
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponce)
def create_post(post: schemas.PostCreate, 
                db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())  # Use the user_id extracted from the token
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#get post path operation end-point
@router.get("/", response_model=List[schemas.PostResponce])
def get_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts

#get post by id end-point
@router.get('/{id}', response_model=schemas.PostResponce)
def get_post_by_id(id : int, 
                   db : Session = Depends(get_db),
                   current_user : models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorised to perform requested action"
        )
    return post

#delete post by id end-point
@router.delete('/{id}')
def post_deletion(id : int,
                  db : Session = Depends(get_db),
                  current_user : models.User = Depends(oauth2.get_current_user)):
    
    # print(f"current user : {current_user}")
    # print(f"current user_id : {current_user.id}")
    # print(f"current user_email : {current_user.email}")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f"post with id : {id} does not exist"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorised to perform requested action"
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
    
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authorised to perform requested action"
        )
    
    post_query.update(update_post.model_dump(), synchronize_session=False)
    db.commit()
    return {'status' : 'post updated successfully'}