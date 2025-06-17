from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from models import Jobtype, employment_type
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str]
    is_active: Optional[bool] = True
    experience: Optional[str]
    cv: Optional[str]
    linkedin_url: Optional[HttpUrl]

class UserCreate(UserBase):
    password: str  # when creating user

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Admin(BaseModel):
    name:str
    email: str
    is_hiring: bool

class JobBase(BaseModel):
    company:str
    role:str
    description:str
    salary : int 
    location: str
    type: Jobtype=Jobtype.hybrid
    worker_type: employment_type = employment_type.full_time
    experience: str
    industry: str
    posted_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    is_avaible:bool = True

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int

class Config:
    orm_mode = True

