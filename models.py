# Models.py is used to create tables and columns structure.

from email.policy import default
from enum import unique
from importlib.machinery import FrozenImporter
from sqlalchemy import Boolean,Column,Integer,String,ForeignKey 
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__='users'
    
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String, unique=True, index=True)
    username= Column(String, unique=True,index=True)
    firstname=Column(String)
    lastname=Column(String)
    hashedpassword=Column(String)
    is_active=Column(Boolean, default=True)

    todos=relationship('Todos',back_populates='owner')


class Todos(Base):
    __tablename__='todos'

    id = Column(Integer,primary_key=True,index=True)
    title=Column(String)
    description=Column(String)
    priority=Column(Integer)
    complete=Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey("users.id"))
    owner=relationship('Users',back_populates='todos')
