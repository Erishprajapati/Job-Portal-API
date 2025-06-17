from database import Base
from sqlalchemy import Column,String, Boolean, Integer, Text, DateTime
from enum import Enum
from sqlalchemy.sql import func
from sqlalchemy import Enum as SQLAlchemyEnum
from pydantic import EmailStr
#this is just to ensure the jobs have 2 types
class Jobtype(str, Enum):
    remote = "remote"
    hybrid = "hybrid"

class employment_type(str, Enum):
    full_time = 'full_time'
    contract_based = "contract_based"
    internship = "internship"
    fellowship = "fellowship"

class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100))
    role = Column(String(100))
    description = Column(Text)
    salary = Column(Integer)
    location = Column(String(100))
    type = Column(SQLAlchemyEnum(Jobtype), default = Jobtype.remote)
    worker_type = Column(SQLAlchemyEnum(employment_type), default = employment_type.full_time)
    experience = Column(String(100))
    industry= Column(String(100))
    posted_at = Column(DateTime(timezone = True), server_default=func.now())
    deadline = Column(DateTime(timezone=True))
    is_available = Column(Boolean, default=True)

    def __repr__(self):
        print(f'{self.role} at {self.company}')

class User(Base):
    __tablename__ ="applicants"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100))
    phone_number = Column(Integer)
    is_active = Column(Boolean, default=True)
    experience = Column(String(100))
    cv = Column(String(200))
    linkedin_url = Column(String(100))

class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    is_hiring = Column(Boolean)
