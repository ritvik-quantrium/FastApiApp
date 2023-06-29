# pip install "fastapi[all]"
# pip install "psycopg[all]"

# pip install "passlib[bcrypt]"
#new main
from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import List, Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
import random 
from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import SessionLocal, engine,get_db
from .routers import post,user,auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# #OLD Database connection

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost" ,database = "fastapiapp" , user="postgres",password = "password",cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connection Failed") 
#     time.sleep(random.randint(2,10))





@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)











 
















# uvicorn main:app --reload


# uvicorn app.main:app --reload
