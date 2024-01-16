from .. import models, schemas, oauth2
from .. import models, schemas, utils
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
from typing import List



router=APIRouter(
    prefix="/admins",
    tags=['Admins']
)



#create admin endpoint

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminOut)

def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):

    #hash the password - admin.password
    hashed_password=utils.hash(admin.password)
    admin.password=hashed_password

    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin




#get all admins endpoint

@router.get('/', response_model=List[schemas.AdminOut])

def get_all_admins(db: Session = Depends(get_db)):

    admins = db.query(models.Admin).all()
    return admins



#get admin by id endpoint

@router.get('/{id}',response_model=schemas.AdminOut)

def get_admin(id:int,db: Session = Depends(get_db)):

    admin= db.query(models.Admin).filter(models.Admin.id==id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Admin with id: {id} does not exist")
    return admin




#delete admin endpoint

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(id: int,db: Session = Depends(get_db)):

    alert_query=db.query(models.Admin).filter(models.Admin.id==id)

    alert=alert_query.first()

    if alert==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin with id: {id} does not exist")

    alert_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)