from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

"""this is to connect with database where 
postgres is user and localhost is port 
and connection is database name """
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:4696@localhost/jobportal" 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind = engine, autoflush= False, autocommit = False)

Base = declarative_base()