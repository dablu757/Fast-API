from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import schemas
import models
import utils
from .import oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.TokenResponce)
def login(user_credential : OAuth2PasswordRequestForm = Depends(),
           db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credential"
        )

    if not utils.varify(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credential"
        )
    
    # 1. create token
    access_token = oauth2.create_access_token(data={'user_id' : user.id})
    # 2. return token
    # return access_token
    return {'access_token' : access_token, 'token_type' : 'bearer'}


