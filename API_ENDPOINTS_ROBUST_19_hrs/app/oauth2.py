from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends,status,HTTPException
from . import schemas,database , models
from sqlalchemy.orm import Session
from .config import setting
from fastapi.security import OAuth2PasswordBearer
# SECRET KEY 
# ALGORITHM
# Expiration Time 
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes



def create_access_token(data:dict):
    encode_data = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode_data.update({"exp":expire})
    jwtencoded = jwt.encode(encode_data,SECRET_KEY ,algorithm=ALGORITHM)
    return jwtencoded


def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data


#pass this as an dependecy(get id from token and check whether token is correct)
def get_current_user(token:str=Depends(oauth2_schema),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"Could not verify credentails" , headers={"WWW_Authenticate":"Bearer"})
    token = verify_access_token(token=token , credentials_exception=credentials_exception)
    # print("token id")
    # print(token.id)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    # print(user.id)

    return user
    # return verify_access_token(token , credentials_exception)