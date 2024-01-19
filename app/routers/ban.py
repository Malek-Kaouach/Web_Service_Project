from sqlalchemy import func
from .. import models, schemas, oauth2
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from ..database import get_db



router=APIRouter()


# Ban user by ID

@router.put("/ban/{id}",response_model=schemas.UserOut)
def ban_user(id:int, db: Session = Depends(get_db),
                 current_admin: int = Depends(oauth2.get_current_admin)):

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    if user.is_banned==True:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"User with id: {id} is already banned")

    # Update the user's is_banned column to True
    user.is_banned = True
    db.commit()

    return user



# Unban user by ID

@router.put("/unban/{id}",response_model=schemas.UserOut)
def unban_user(id:int, db: Session = Depends(get_db),
                 current_admin: int = Depends(oauth2.get_current_admin)):

    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    if user.is_banned==False:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail=f"User with id: {id} is already active")

    # Update the user's is_banned column to False
    user.is_banned = False
    db.commit()

    return user