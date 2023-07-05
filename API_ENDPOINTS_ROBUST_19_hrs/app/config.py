
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname : Optional[str]
    database_port : Optional[str] 
    database_password: Optional[str] 
    database_name: Optional[str] 
    database_username: Optional[str] 
    secret_key: Optional[str] 
    algorithm: Optional[str] 
    access_token_expire_minutes: Optional[int]

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

setting = Settings()
# setting = Settings(_env_file='prod.env', _env_file_encoding='utf-8')