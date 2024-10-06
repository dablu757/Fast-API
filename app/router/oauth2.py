from jose import JWTError, jwt
from datetime import datetime, timedelta

'''
there are 3 thing are required for generating a jwt token
1. SECRET_KEY
2. HASHING_ALGORITHM
3. EXPIRATION_TIME

'''

SECRET_KEY = "98a5006892445eead3ba932c239a24b51b54683c240ca7fdff6896466257b6f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict)->str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp' : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

