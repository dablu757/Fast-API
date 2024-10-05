from fastapi import status,HTTPException,Depends, APIRouter
import schemas, models, utils
# from app import schemas, utils, models
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix="/user"
)

#create user path operation end-point
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def user_create(user : schemas.UserCreate, db : Session = Depends(get_db)):

    #hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_users = models.User(**user.model_dump())
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    return new_users

#get user by id end-point
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db :Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found"
        )
    
    return user
