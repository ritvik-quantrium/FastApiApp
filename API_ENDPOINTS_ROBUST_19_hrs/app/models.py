from .database import Base 
from sqlalchemy import Boolean, Column, ForeignKey,Integer,String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer,primary_key = True , nullable = False)
    title = Column(String,nullable = False )
    content = Column(String , nullable=False)
    published = Column(Boolean , nullable=False , server_default = 'TRUE') 
    created_at = Column(TIMESTAMP(timezone=True),nullable = False , server_default =text("now()"))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE") , nullable = False)


#new sqlalchemy model 
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key = True  ,nullable = False )
    email = Column(String,nullable = False ,unique=True)
    password = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False , server_default =text("now()"))



    




