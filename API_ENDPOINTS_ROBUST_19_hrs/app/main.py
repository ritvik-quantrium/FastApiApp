# pip install "fastapi[all]"
# pip install "psycopg[all]"







from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import random 



app = FastAPI()
class Post(BaseModel):
    title:str 
    content :str
    published : bool = True 


#Database connection

while True:
    try:
        conn = psycopg2.connect(host="localhost" ,database = "fastapiapp" , user="postgres",password = "",cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection Failed")
    time.sleep(random.randint(2,10))












Sample_Data = [
    {"title": "Title of Post 1" ,"content":"content of Post 1","id":1} ,
    {"title": "favorite" ,"content":"content of Post 1","id":2} ,
]
def utitlty_for_post(id):
    for p in Sample_Data:
        if p["id"]==id:
            return p 
    return None
def index_for_post(id):
    itr = 0 
    for p in Sample_Data:
        if p["id"]==id:
            return itr
        itr+=1
    return None



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM post""")
    post = cursor.fetchall()
    return {"data":post}




@app.get("/posts/{id}")
def get_posts(id:int ):
    cursor.execute("""SELECT * from post WHERE id = %s""" ,(str(id),))
    # post = cursor.fetchall()
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")

    return {"post_detail":post}

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
def create_posts(post:Post):
    cursor.execute("""INSERT INTO post(title, content, published) VALUES(%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    #commit changes 
    conn.commit()


    # post_dict = post.dict()
    # post_dict["id"] = randrange(0,1000000)
    # Sample_Data.append(post_dict)
    return {"data":new_post}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):



    cursor.execute("""DELETE FROM post WHERE id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204

    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # Sample_Data.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204




@app.put("/posts/{id}")
def update_post(id:int , post:Post):


    
    cursor.execute("""UPDATE post SET title = %s ,content = %s , published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id),))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id = {id} was not found")

    return {'data':updated_post} 



    # index = index_for_post(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    # cur_post = post.dict()
    # cur_post["id"] = id
    # Sample_Data[index] = cur_post
    # return {'data':cur_post} # cant send back any data when STATUS CODE is 204


# uvicorn main:app --reload
























