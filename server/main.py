from fastapi import FastAPI
import schemas, database, models
from .database import declarative_base, Base, SessionLocal



#making the instance of the app
app = FastAPI()

#TODO: this code was just to check the direction of homepage
# @app.get('/')
# def home():
#     return "hey"

def get_database():
    db = SessionLocal()  #TODO: fix this Sessionlocal story
    try:
        yield db
    finally:
        db.close()

