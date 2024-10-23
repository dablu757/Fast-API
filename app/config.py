import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    database_host = os.getenv("DATABASE_HOSTNAME")
    database_port = os.getenv("DATABASE_PORT")
    database_user = os.getenv("DATAABSE_USER_NAME")
    database_password = os.getenv("DATABASE_PASSWORD")
    database_name = os.getenv("DATABASE_NAME")
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

settings = Settings()