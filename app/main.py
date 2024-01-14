from fastapi import FastAPI
from . import models
from .database import engine
from .routers import alert,user,auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(alert.router)
app.include_router(user.router)
app.include_router(auth.router)




# @app.get("/")
# def get_user():
#     return {"message":"Welcome to my api malek"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     print(posts)
#     return{"data":"successfull"}




