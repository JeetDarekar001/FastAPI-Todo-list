
from pyexpat import model
from tokenize import TokenInfo
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import Depends
from typing import Optional
from pydantic import BaseModel,Field  
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from auth import get_current_user ,get_user_exception

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

# Class to use for post which depends upon the Todos in models.py
class Todo(BaseModel):
    title:str
    description:Optional[str]
    priority:int
    complete:bool 


@app.get("/")
async def read_all_todos(db:Session=Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/todo/{todoid}")
async def get_todo_by_ID(todoid : int,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()

    todo_model=db.query(models.Todos)\
        .filter(models.Todos.id==todoid)\
        .filter(models.Todos.owner_id==user.get("id"))\
        .all()
    if todo_model is not None:
        return todo_model
    raise http_exception()

@app.get("/todos/user")
async def read_all_by_user(user:dict=Depends(get_current_user) , db:Session=Depends(get_db)):
    if user is None:
        raise get_user_exception()
     
    return db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()


@app.post("/")
async def create_todo(todo:Todo,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user is None:
        raise  get_user_exception()
    print(todo)
    todo_model=models.Todos()
    todo_model.title=todo.title
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete
    todo_model.owner_id=user.get('id')
    
    db.add(todo_model)
    db.commit()

    return success_response(200)

@app.put("/{todo_id}")
async def update_todo(todo_id:int,todo:Todo, 
                      user:dict=Depends(get_current_user),
                      db:Session=Depends(get_db)):

    if user is None:
        raise get_user_exception()
        
    todo_model=db.query(models.Todos)\
        .filter(models.Todos.id==todo_id)\
        .filter(models.Todos.owner_id==user.get('id'))\
        .first()


    if todo_model is None:
        raise http_exception()

    todo_model.title=todo.title
    todo_model.desciption=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete
    

    db.add(todo_model)
    db.commit()
    return success_response(200)

@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,
                    user:dict=Depends(get_current_user),
                    db:Session=Depends(get_db)):
                    
    if user is None:
        raise get_user_exception()                
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).filter(models.Todos.owner_id==user.get("id")).all()
    if todo_model is None:
        raise http_exception()
    db.query(models.Todos).filter(models.Todos.id==todo_id).delete()
    db.commit()
    return success_response(200)


def success_response(status_code:int):
    return {
        "status":status_code,
        'transaction':'successfull'
    }

def http_exception():
    raise HTTPException(status_code=404,detail="Todo Not Found")
    
