from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional,List
app = FastAPI()

users = []



class User(BaseModel):
    email:str 
    isactive : bool 
    google: Optional[str]



@app.get("/users" , response_model=List[User])
async def get_users():
    return users


@app.post("/users")
async def create_root(user:User):
    users.append(user)
    return "Suckess"

@app.get("/users/{id}")
async def get_user(id : int):
    return users[id]


