from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://dabluchauhan:postgresql@localhost:8080/fastapi"



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# this function create a seassion for every request 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# print("database file run successfuly")