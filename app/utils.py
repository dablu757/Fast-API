from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def hash(password : str)->str:
    return pwd_context.hash(password)

def varify(plant_password : str, hashed_password : str)->bool:
    return pwd_context.verify(plant_password, hashed_password)
