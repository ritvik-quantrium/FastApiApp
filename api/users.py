from fastapi import FastAPI,Path,Query,APIRouter
from pydantic import BaseModel
from typing import Optional,List


router = APIRouter()

users = []


class User(BaseModel):
    email:str 
    isactive : bool 
    google: Optional[str]



@router.get("/users" , response_model=List[User])
async def get_users():
    return users


@router.post("/users")
async def create_root(user:User):
    users.append(user)
    return "Success"

# @router.get("/users/{id}")
# async def get_user(
#         id : int=Path(...,description="The ID of the users you want (gt>2) by Ritvik",ge=0),
#         q: str=Query(None , max_length=5)
#     ):
#     return {"user":users[id],"query":q}
@router.get("/users/{id}")
async def get_user(
        id : int
    ):
    return {"user":users[id]}
