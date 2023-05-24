# pip install "fastapi[all]"








from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
app = FastAPI()
class Post(BaseModel):
    title:str 
    content :str
    published : bool = True 
    rating : Optional[int]=None



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data":"This is your pets"}



@app.post("/posts")
def create_pots(post:Post):
    return {"mew_post":f"title {post['title']} content: {post['content']}"}


# uvicorn main:app --reload


























