from os import stat
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import Depends
from typing import Optional
from pydantic import BaseModel,Field  
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

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
    priority:int=Field(gt=0,lt=100,description="The priority must be between 1-10")
    complete:bool



@app.get("/")
async def read_all_todos(db:Session=Depends(get_db)):
    return db.query(models.Todos).all()

@app.get("/todo/{todoid}")
async def get_todo_by_ID(todo_id : int,db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos)\
        .filter(models.Todos.id==todo_id)\
        .first()
    if todo_model is not None:
        return todo_model
    raise http_exception()
    
@app.post("/")
async def create_todo(todo:Todo,db:Session=Depends(get_db)):
    todo_model=models.Todos()
    todo_model.title=todo.title
    todo_model.desciption=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()

    return {
        "status":201,
        'transaction':'successfull'
    }

@app.put("/{todo_id}")
async def update_todo(todo_id:int,todo:Todo,db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos)\
        .filter(models.Todos.id==todo_id)\
        .first()

    if todo_model is None:
        raise http_exception()

    todo_model.title=todo.title
    todo_model.desciption=todo.description
    todo_model.priority=todo.priority
    todo_model.complete=todo.complete

    db.add(todo_model)
    db.commit()
    return {
        "status":201,
        'transaction':'successfull'
    }

@app.delete("/{todo_id}")
async def delete_todo(todo_id:int, db:Session=Depends(get_db)):
    todo_model=db.query(models.Todos).filter(models.Todos.id==todo_id).first()
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
    
