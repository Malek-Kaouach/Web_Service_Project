from .. import models, schemas, utils, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db
from typing import List, Optional

from app.utils import verify



router=APIRouter(
    prefix="/users",
    tags=['Users']
)


# Create user endpoint

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



# Get user by id endpoint

@router.get('/{id}',response_model=schemas.UserOut4Admin)
def get_user(id:int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return user



# Get all users endpoint

@router.get('/', response_model=List[schemas.UserOut4Admin])

def get_all_users(db: Session = Depends(get_db),
                  current_admin: int = Depends(oauth2.get_current_admin),
                  limit: Optional[int]=100, skip: Optional[int]=0,
                  search: Optional[str]= ""): #search filter by phone number

    users = db.query(models.User).filter(models.User.phone_number.contains(search)).limit(limit).offset(skip).all()
    return users



# Get current user personal info

@router.get('/info/{id}',response_model=schemas.UserDetails)
def get_current_user_information(id:int, user_pwd: schemas.UserPWD, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user= db.query(models.User).filter(models.User.id==id).first()
    #add code for dehashing the password

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    
    if user.id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    if verify(user_pwd.password, user.password):
        # Create a new instance of UserDetails with the dehashed password
        user_details = schemas.UserDetails(**user.__dict__)
        user_details.password = user_pwd.password

        return user_details

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")




# Delete user endpoint

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    user_query=db.query(models.User).filter(models.User.id==id)
    user_del=user_query.first()

    if user_del==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update user by ID endpoint

@router.put("/{id}",response_model=schemas.UserOut)
def update_user(id:int, user: schemas.UserCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    #hash the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    user_query=db.query(models.User).filter(models.User.id==id)
    user_2update=user_query.first()

    if user_2update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    if user_2update.id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    user_query.update(user.dict(),synchronize_session=False)
    db.commit()

    return user_query.first()


"""
# Update password of current user endpoint

@router.put("/pwd/{id}",response_model=schemas.UserOut)
def update_pwd(id:int, user: schemas.UserPWD, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    
    #hash the password - user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    user_query=db.query(models.User).filter(models.User.id==id)
    user_2update=user_query.first()

    if user_2update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    
    if user_2update.id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    user_query.update(user.dict(),synchronize_session=False)
    db.commit()

    return user_query.first()
"""

