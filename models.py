# Models.py is used to create tables and columns structure.

from email.policy import default
from xmlrpc.client import Boolean
from sqlalchemy import Boolean,Column,Integer,String
from database import Base

class Todos(Base):

    __tablename__='todos'

    id = Column(Integer,primary_key=True,index=True)
    title=Column(String)
    desciption=Column(String)
    priority=Column(Boolean)
    complete=Column(Boolean,default=False)


