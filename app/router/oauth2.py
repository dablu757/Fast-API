from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
import schemas
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import models
from database import get_db
from sqlalchemy.orm import Session
from config import settings

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

'''
there are 3 thing are required for generating a jwt token
1. SECRET_KEY
2. HASHING_ALGORITHM
3. EXPIRATION_TIME

'''

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)

#create token
def create_access_token(data : dict)->str:
    to_encode = data.copy()
    # expire = datetime.now(datetime.utc())+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#verify token
def verify_access_token(token : str, credentials_exception):
    try:
        #decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #extract id from payload
        id : str = payload.get('user_id')
        if not id :
            raise credentials_exception
        #validate data from schema 
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    
    return token_data


#get curretn user
def get_current_user(token : str = Depends(oath2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    # print(f"token data : {token_data}")
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    # print(f"user : {user}")
    return user