from pyexpat import model
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
