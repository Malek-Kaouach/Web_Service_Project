from .. import models, schemas, utils, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
from typing import List, Optional



router=APIRouter(
    prefix="/users",
    tags=['Users']
)


# create user endpoint

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# get user by id endpoint

@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return user



#get all users endpoint

@router.get('/', response_model=List[schemas.UserOut])

def get_all_users(db: Session = Depends(get_db),
                  current_admin: int = Depends(oauth2.get_current_admin),
                  limit: Optional[int]=100, skip: Optional[int]=0,
                  search: Optional[str]= ""): #search filter by phone number

    users = db.query(models.User).filter(models.User.phone_number.contains(search)).limit(limit).offset(skip).all()
    return users




#delete user endpoint

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    alert_query=db.query(models.User).filter(models.User.id==id)

    alert=alert_query.first()

    if alert==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    alert_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

