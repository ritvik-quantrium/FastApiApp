
from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal, engine,get_db



router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post("/",status_code=status.HTTP_201_CREATED )
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    ## CREATE HASH OF PASSWORD 
    
    user.password = utils.hash(user.password)

    # new_post = models.Post(title = post.title , content = post.content , published = post.published)
    database_user = db.query(models.User).filter(models.User.email==user.email).first()
    if database_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with id = {user.email} already exist")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user





@router.get("/{id}",response_model=schemas.Userout)
def get_user(id:int,db:Session = Depends(get_db)):
    ## CREATE HASH OF PASSWORD 
    
    user = db.query(models.User).filter(models.User.id==id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} was not found")

    return user


