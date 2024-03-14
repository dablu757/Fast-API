from typing import Optional, List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models,schemas
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

#Data Base
# while True:
#     try : 
#         conn = psycopg2.connect(host = "localhost" , database = "fastapi" , user = "postgres",
#                                  password = "root",cursor_factory = RealDictCursor)

#         con = conn.cursor()
#         print("Database was successfully connected")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error was : ", error)
#         time.sleep(2)


#Get method from data base
@app.get("/posts", response_model= list[schemas.Posts])
def get_posts(db : Session = Depends(get_db)):
    # con.execute(''' SELECT * FROM post''')
    # post=con.fetchall()
    posts = db.query(models.Post).all()
    return posts


# 1 Create post [Data base]
@app.post("/posts",status_code=status.HTTP_201_CREATED , response_model = schemas.Posts)
def create_post(Payload : schemas.CreatePost , db : Session = Depends(get_db)):

#Without ORM
    # con.execute(""" INSERT INTO post (title,content) VALUES(%s,%s) RETURNING * """ ,
    #             (Payload.title , Payload.content))
    
    # new_post = con.fetchone()
    # conn.commit()
    #                                                           
#With ORM
    # new_post = models.Post(title = Payload.title , content = Payload.content , published = Payload.published)
    new_post = models.Post(**Payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
   


#Get indivisioul post
@app.get("/post/{id}", response_model=schemas.Posts)
def get_single_post(id : int, db : Session = Depends(get_db)):
    # con.execute(""" SELECT * FROM post WHERE id = %s """ , (str(id))) 
    # post = con.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if  not post:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"post with id {id} was not found")
        
    return post


#Delete Post
@app.delete("/post/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int ,db : Session = Depends(get_db)):
    # con.execute(""" DELETE  FROM post WHERE id = %s RETURNING * """, (str(id)))
   
    # delete_post = con.fetchone()
    # conn.commit()


    post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT ,
                            details = f"post with id {id} was not found")

    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATE
@app.put("/post/{id}", response_model= schemas.Posts)
def update_post(id : int ,Payload : schemas.CreatePost,  db :Session = Depends(get_db)):
    # con.execute(
    #    """ UPDATE post SET
    #     title = %s,
    #     content = %s,
    #     published = %s WHERE id = %s
    #     returning * """ , (Payload.title , Payload.content , Payload.published , str(id))  
    # )

    # update_post = con.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"post with id {id} was not found")
    
    post_query.update(Payload.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def User_create(user : schemas.UserCreate, db : Session = Depends(get_db)):

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



