


from fastapi import FastAPI
import models
from database import engine
from routers import auth,todos
from company import compantapis

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    compantapis.router,
    prefix="/company",
    tags=["Companyapis"],
    responses={418:{"description":"Internal Use Only"}}
    )
