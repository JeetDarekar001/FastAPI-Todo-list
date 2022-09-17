
import sys


sys.path.append("..")

from fastapi import APIRouter,Depends,HTTPException
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from passlib.context import CryptContext

from routers.auth import get_current_user,get_user_exception,verifyPassword

app=APIRouter()

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

class User(BaseModel):
    username : str
    email : Optional[str]
    first_name:str
    last_name:str
    password:str

class UserVerification(BaseModel):
    username:str
    password:str
    new_password:str

bcrpyt_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return bcrpyt_context.hash(password)



@app.get("/")
async def get_all_user(db:Session=Depends(get_db)):

    return db.query(models.Users).all()

@app.get("/{username}")
async def get_user_by_username(username:str,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.username==username).all()
    return user

@app.post("/create/")
async def create_user(create_user:User,db:Session=Depends(get_db)):
    create_user_model=models.Users()
    create_user_model.email=create_user.email
    create_user_model.username=create_user.username
    create_user_model.firstname=create_user.first_name
    create_user_model.lastname=create_user.last_name
    create_user_model.hashedpassword=get_password_hash(create_user.password)
    create_user_model.is_active=True
    try:

        db.add(create_user_model)
        db.commit()
        return {'Success':"user Created"}
    except Exception as e :
        raise HTTPException(status_code=500,detail=f'Username/Email Already Present={e}')


@app.put("/password")
async def user_password_change(user_verification:UserVerification,user:dict=Depends(get_current_user),
            db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception
    user_model=db.query(models.Users).filter(models.Users.id==user.get('id')).first()
    if user_model is not None:
        if user_verification.username == user_model.username and verifyPassword(user_verification.password,user_model.hashedpassword):
            user_model.hashedpassword=get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "successfull"
    raise get_user_exception()


@app.delete("/")
async def delete_user(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        return get_user_exception()    

    user_model=db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is None:
        raise get_user_exception()
    db.query(models.Users).filter(models.Users.id==user.get("id")).delete()
    db.commit()
    return "Successfull"