from .. import models, schemas, oauth2
from .. import models, schemas, utils
from fastapi import Header, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
from typing import List, Optional

from ..config import settings


router=APIRouter(
    prefix="/admins",
    tags=['Admins']
)

#ADMIN KEY
ADMINKEY=settings.adminkey

# Create admin endpoint

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)

def create_admin(admin: schemas.AdminCreate, key: str=Header(...) , db: Session = Depends(get_db)):

    #verify adminkey to create the admin
    if key != ADMINKEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Main Key")

    #hash the password - admin.password
    hashed_password=utils.hash(admin.password)
    admin.password=hashed_password

    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)   
    db.commit()
    db.refresh(new_admin)
    return new_admin



# Get all admins endpoint

@router.get('/', response_model=List[schemas.AdminOut])

def get_all_admins(db: Session = Depends(get_db),
                   current_admin: int = Depends(oauth2.get_current_admin),
                   limit: Optional[int]=100, skip: Optional[int]=0,
                   search: Optional[str]= ""): #search filter by admin name

    admins = db.query(models.Admin).filter(models.Admin.name.contains(search)).limit(limit).offset(skip).all()
    return admins



# Get admin by id endpoint

@router.get('/{id}',response_model=schemas.AdminOut)

def get_admin(id:int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    admin= db.query(models.Admin).filter(models.Admin.id==id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Admin with id: {id} does not exist")
    return admin




# Delete admin endpoint

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    admin_query=db.query(models.Admin).filter(models.Admin.id==id)
    admin_2delete=admin_query.first()

    if admin_2delete==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with id: {id} does not exist")

    admin_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update admin by ID endpoint

@router.put("/{id}",response_model=schemas.AdminOut)
def update_admin(id:int, admin: schemas.AdminCreate, db: Session = Depends(get_db),
                 current_admin: int = Depends(oauth2.get_current_admin)):
    
    #hash the password - admin.password
    hashed_password=utils.hash(admin.password)
    admin.password=hashed_password

    admin_query=db.query(models.Admin).filter(models.Admin.id==id)
    admin_2update=admin_query.first()

    if admin_2update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with id: {id} does not exist")

    admin_query.update(admin.dict(),synchronize_session=False)
    db.commit()

    return admin_query.first()



# Update current status of admin by ID endpoint

@router.put("/status/{id}",response_model=schemas.AdminOut)
def update_admin(id:int, admin: schemas.AdminStatus, db: Session = Depends(get_db),
                 current_admin: int = Depends(oauth2.get_current_admin)):

    admin_query=db.query(models.Admin).filter(models.Admin.id==id)
    admin_2update=admin_query.first()

    if admin_2update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with id: {id} does not exist")

    admin_query.update(admin.dict(),synchronize_session=False)
    db.commit()

    return admin_query.first()