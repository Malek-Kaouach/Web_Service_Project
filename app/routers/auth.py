from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils, oauth2
from ..database import get_db



router=APIRouter(tags=['Authentication'])


# Login admin and user endpoint
"""
@router.post('/loginuser',response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):

    user= db.query(models.User).filter(models.User.phone_number== user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create an access token
    access_token=oauth2.create_access_token(data={"user_id": user.id})

    #return a token
    return {"access_token": access_token, "token_type": "bearer"}




@router.post('/loginadmin',response_model=schemas.Token)
def login_admin(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):

    admin= db.query(models.Admin).filter(models.Admin.id== user_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create an access token
    access_token=oauth2.create_access_token(data={"admin_id": admin.id})

    #return a token
    return {"access_token": access_token, "token_type": "bearer"}
 """ 

# When using 2 endpoints for the login we can't make sure that always one token can exist
# As a solution we will fuse both endpoints to achieve login for both user and admin from the same endpoint while having always one token
# The reason of having one token is for security reasons: YOU CAN'T BE AUTHENTICATED FOR BEING AS USER AND ADMIN AT THE SAME TIME

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.phone_number == user_credentials.username).first()
    admin = db.query(models.Admin).filter(models.Admin.id == user_credentials.username).first()

    if not user and not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if user:
        if not utils.verify(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        id = user.id
        # Create an access token
        access_token = oauth2.create_access_token(data={"user_id": id})
    else:
        if not utils.verify(user_credentials.password, admin.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
        id = admin.id
        # Create an access token
        access_token = oauth2.create_access_token(data={"admin_id": id})

    # Return the token
    return {"id": id,"access_token": access_token, "token_type": "bearer"}
    