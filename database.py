from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


#SQLALCHEMY_DATABSE_URL="sqlite:///./todos.db"

#engine=create_engine(
#   SQLALCHEMY_DATABSE_URL,
#    connect_args={"check_same_thread":False}
#)

SQLALCHEMY_DATABSE_URL="postgresql://postgres:test1234@localhost/TodoApplicationDatabase"

engine=create_engine(
    SQLALCHEMY_DATABSE_URL
)


SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base= declarative_base()
# Base will allows us to call each database model. 
# We will inherit the base in future files




