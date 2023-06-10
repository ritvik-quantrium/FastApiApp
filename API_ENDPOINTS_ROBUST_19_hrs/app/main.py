# pip install "fastapi[all]"








from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
app = FastAPI()
class Post(BaseModel):
    title:str 
    content :str
    published : bool = True 
    rating : Optional[int]=None

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
    return {"data":Sample_Data}




@app.get("/posts/{id}")
def get_posts(id:int ,response:Response):
    post = utitlty_for_post((int)(id))
    if not post:
        # response.status_code = 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message"}

    # return {"post_detail":f"Here is post {id}"}
    return {"post_detail":post}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    Sample_Data.append(post_dict)
    return {"data":post_dict}



@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    index = index_for_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    Sample_Data.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # cant send back any data when STATUS CODE is 204




@app.put("/posts/{id}")
def update_post(id:int , post:Post):
    index = index_for_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")

    cur_post = post.dict()
    cur_post["id"] = id
    Sample_Data[index] = cur_post
    return {'data':cur_post} # cant send back any data when STATUS CODE is 204


    return 
# uvicorn main:app --reload
























