from fastapi import Depends, FastAPI, HTTPException, status
import schemas, database, models, hashing
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import Admin, Job, User
from hashing import Hash



#making the instance of the app
app = FastAPI()

#TODO: this code was just to check the direction of homepage
# @app.get('/')
# def home():
#     return "hey"

def get_database():
    db = SessionLocal()  
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=engine)

@app.post('/create_admin', status_code = status.HTTP_201_CREATED, tags=["Admin"])
def create_admin(request: schemas.Admin, db:Session= Depends(get_database)):
    existing_admin = db.query(models.Admin).filter(models.Admin.email == request.email).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Admin already exists with this email"
        )
    new_admin = models.Admin(
        name = request.name,
        email = request.email,
        password = hashing.Hash.bcrypt(request.password),
        is_hiring = request.is_hiring
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
    
"""
Showing the list of admin 
"""
@app.get('/show_admins', tags=["Admin"])
def show_admins(db:Session= Depends(get_database))->None:
    admins = db.query(models.Admin).all()
    return admins

@app.put('/admin/{admin_id}/update', tags = ["Admin"])
def update_admin(admin_id:int, request: schemas.Admin, db:Session= Depends(get_database)):
    admin_updated = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin_updated:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = "failed to update the admin"
        )
    admin_updated.name = request.name
    admin_updated.email = request.email
    admin_updated.password = hashing.Hash.bcrypt(request.password)
    admin_updated.is_hiring = request.is_hiring
    db.commit()
    db.refresh(admin_updated)
    return {"admin_updated": True, "message": f"Admin updated successfully for id {admin_id}"}

"""
Deleting the admin
"""
@app.delete('/admin/{admin_id}/delete', tags=["Admin"])
def delete_admin(admin_id:int, db:Session= Depends(get_database)):
    db.query(models.Admin).filter(models.Admin.id == admin_id).delete(synchronize_session=False)
    db.commit()
    return 'Admin deleted succesfully'


""""lets work for user"""
@app.post('/home', status_code=status.HTTP_201_CREATED, tags=["Users"])
def register_user(request: schemas.UserBase, db:Session = Depends(get_database)):
    existing_user = db.query(models.User).filter(models.User.email == request.email and models.User.phone_number == request.phone_number).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = 'User already existed..'
        )
    new_user = models.User(
        full_name = request.full_name,
        email = request.email,
        phone_number = request.phone_number,
        is_active = request.is_active,
        experience = request.experience,
        cv = request.cv,
        linkedin_url = str(User.linkedin_url) 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User created successfully for {new_user.full_name}"}

@app.get('/home/all_users', tags=["Users"])
def all_users(db:schemas = Depends(get_database)):
    users = db.query(models.User).all()
    return users
"""
update the user
"""
@app.put('/home/{user_id}/update', tags=["Users"])
def update_user(user_id:int, request: schemas.UserBase, db:Session = Depends(get_database)):
    updated_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail = 'User update failed'
        )
    updated_user.full_name = request.full_name
    updated_user.email = request.email
    updated_user.phone_number = request.phone_number
    updated_user.is_active = request.is_active
    updated_user.experience = request.experience
    updated_user.cv = request.cv
    updated_user.linkedin_url = str(request.linkedin_url)

    db.commit()
    db.refresh(updated_user)
    return {"message": f"User information updated for {updated_user.full_name} with id {user_id}"}


@app.delete('/home/delete/{user_id}', tags=["Users"])
def delete_user(user_id:int, db:Session = Depends(get_database)):
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return {"message" : f"User with {user_id} deleted succesfully"}

"""
Crud for jobs
"""
@app.post('/home/add_jobs', tags=["Jobs"])
def create_jobs(request: schemas.JobBase, db:Session = Depends(get_database)):
    existing_jobs = db.query(models.Job).filter(models.Job.company == request.company and models.Job.role == request.role and models.Job.description == request.description).first()
    if existing_jobs:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            details = "Job exists with these information..."
        )
    add_job = models.Job(
        company = request.company,
        role = request.role,
        description = request.description,
        salary = request.salary,
        location = request.location,
        type = request.type,
        worker_type = request.worker_type,
        experience = request.experience,
        industry = request.industry, 
        posted_at = request.posted_at,
        deadline = request.deadline,
        is_available = request.is_available
    )
    db.add(add_job)
    db.commit()
    db.refresh(add_job)
    return {"message" : f"Job added fpr {request.company} for the role of {request.role}"}

@app.get('/home/all_jobs', tags=['Jobs'])
def show_jobs(db:Session = Depends(get_database)):
    all_jobs = db.query(models.Job).all()
    return all_jobs

#update jobs
@app.put('/home/update_jobs/{job_id}', tags=['Jobs'])
def update_jobs(job_id: int, request: schemas.JobBase, db:Session = Depends(get_database)):
    jobs = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not jobs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            details = f"Job not found for {job_id}"
        )
    jobs.company = request.company
    jobs.role = request.role
    jobs.description = request.description
    jobs.salary = request.salary
    jobs.location = request.location
    jobs.type = request.type
    jobs.worker_type = request.worker_type
    jobs.experience = request.experience
    jobs.industry = request.industry
    jobs.posted_at = request.posted_at
    jobs.deadline = request.deadline
    jobs.is_available = request.is_available

    db.commit()
    db.refresh(jobs)
    return {"Message" : f"Job information updated for {request.company}"}

