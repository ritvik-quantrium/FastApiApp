# pip install "fastapi[all]"
# pip install "psycopg[all]"


#new main
from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import random 
from sqlalchemy.orm import Session
from . import models 
from .database import SessionLocal, engine,get_db
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}



class Post(BaseModel):
    title:str 
    content :str
    published : bool = True 

#OLD Database connection

while True:
    try:
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection Failed")
    time.sleep(random.randint(2,10))





@app.get("/")
async def root():
    return {"message": "Hello World"}





@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM post""")
    # post = cursor.fetchall()

    posts = db.query(models.Post).all()


    # posts = db.query(models.Post)
    # print(posts)# will return query
    return {"data":posts}




 



@app.get("/posts/{id}")
def get_posts(id:int,db:Session = Depends(get_db) ):


    post = db.query(models.Post).filter(models.Post.id==id).first() #instead of looking everywhere just return first and stop
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")

    return {"post_detail":post}






    # USING DIRECT POSTGRES CONNECTION
    '''

        cursor.execute("""SELECT * from post WHERE id = %s""" ,(str(id),))
        # post = cursor.fetchall()
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")

        return {"post_detail":post}
    '''
    # USING SAMPLE DATABASE
    '''
    post = utitlty_for_post((int)(id))
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message"}

    # return {"post_detail":f"Here is post {id}"}
    return {"post_detail":post}'''


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post,db:Session = Depends(get_db)):


    # new_post = models.Post(title = post.title , content = post.content , published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}




    # cursor.execute("""INSERT INTO post(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # #commit changes 
    # conn.commit()


    # post_dict = post.dict()
    # post_dict["id"] = randrange(0,1000000)
    # Sample_Data.append(post_dict)
    # return {"data":new_post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int,db:Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id ==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()

    #USING direct postgres connection
    # cursor.execute("""DELETE FROM post WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    # return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204
    #USING sample database
    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # Sample_Data.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204




@app.put("/posts/{id}")
def update_post(id:int , updatedpost:Post,db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")
    post_query.update(updatedpost.dict() , synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}




    #Update Postgres using direct connection
    # cursor.execute("""UPDATE post SET title = %s ,content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()

    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    # return {'data':updated_post} 


    #Update Sample Data
    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # cur_post = post.dict()
    # cur_post["id"] = id
    # Sample_Data[index] = cur_post
    # return {'data':cur_post} # cant send back any data when STATUS CODE is 204


# uvicorn main:app --reload


# uvicorn app.main:app --reload
