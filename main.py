from fastapi import HTTPException
from fastapi import FastAPI
from fastapi import Depends
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
    
def http_exception():
    raise HTTPException(status_code=404,detail="Todo Not Found")