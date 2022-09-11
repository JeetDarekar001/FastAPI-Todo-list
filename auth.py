
from datetime import datetime, timedelta
from fastapi import FastAPI,Depends, HTTPException,status
from pydantic import BaseModel
from typing import Optional
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt , JWTError

SECRET_KEY = "TESTABHIJIT"
ALGORITHM = "HS256"

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")
# Dependcy ; which is going to extract auth from header
def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

class CreateUser(BaseModel):
    username : str
    email : Optional[str]
    first_name:str
    last_name:str
    password:str


bcrpyt_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return bcrpyt_context.hash(password)

def verifyPassword(plain_password, hash_password):
    return bcrpyt_context.verify(plain_password,hash_password)

def auth_user(username:str,password:str,db):
    user=db.query(models.Users)\
        .filter(models.Users.username==username)\
            .first()
    if not user:
        return False
    if not verifyPassword(password,user.hashedpassword):
        return False
    return user

# Creating New User and adding the details in Databse.
# Password is encrypted using Bcrypt library.

def create_access_token(username:str, user_id :str ,expires_delta : Optional[timedelta] = None):
    encode={"sub":username,"id": user_id}
    if expires_delta :
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token:str = Depends(oauth2_bearer)):
    try:    
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username :str =payload["sub"]
        
        user_id:int = payload['id']

        if username is None or user_id is None:
            raise get_user_exception()
        return {"username":username,"id":user_id}
    except JWTError:
        raise get_user_exception()


@app.post("/create/user")
async def create_user(create_user:CreateUser,db:Session=Depends(get_db)):
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

# Signing using OAuth
@app.post('/token')
async def login_for_access_token(formdata:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=auth_user(formdata.username, formdata.password,db)
    if not user:
        raise token_exception()
    
    token_expires=timedelta( minutes=20 )
    token= create_access_token( user.username, user.id, expires_delta=token_expires)

    return {"token":token}

   

def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response