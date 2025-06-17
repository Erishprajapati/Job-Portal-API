from fastapi import Depends, FastAPI, HTTPException, status
import schemas, database, models
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from models import Admin, Job, User


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

@app.post('/create_admin', status_code = status.HTTP_201_CREATED)
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
        is_hiring = request.is_hiring
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
    
"""
Showing the list of admin 
"""
@app.get('/show_admins')
def show_admins(db:Session= Depends(get_database))->None:
    admins = db.query(models.Admin).all()
    return admins

@app.put('/admin/{admin_id}/update')
def update_admin(admin_id:int, request: schemas.Admin, db:Session= Depends(get_database)):
    admin_updated = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    if not admin_updated:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail = "failed to update the admin"
        )
    admin_updated.name = request.name
    admin_updated.email = request.email
    admin_updated.is_hiring = request.is_hiring
    db.commit()
    db.refresh(admin_updated)
    return {"admin_updated": True, "message": f"Admin updated successfully for id {admin_id}"}

"""
Deleting the admin
"""
@app.delete('/admin/{admin_id}/delete')
def delete_admin(admin_id:int, db:Session= Depends(get_database)):
    db.query(models.Admin).filter(models.Admin.id == admin_id).delete(synchronize_session=False)
    db.commit()
    return 'Admin deleted succesfully'


""""lets work for user"""
@app.post('/home', status_code=status.HTTP_201_CREATED)
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

@app.get('/home/all_users')
def all_users(db:schemas = Depends(get_database)):
    users = db.query(models.User).all()
    return users
"""
update the user
"""
@app.put('/home/{user_id}/update')
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


@app.delete('/home/delete/{user_id}')
def delete_user(user_id:int, db:Session = Depends(get_database)):
    db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)
    db.commit()
    return {"message" : f"User with {user_id} deleted succesfully"}


