from sqlalchemy import func

from .. import models, schemas, oauth2
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List, Optional
from ..database import get_db





router=APIRouter(prefix="/history")




# Get all activity history endpoint

@router.get('/', response_model=List[schemas.HistoryOut])

def get_all_history(db: Session = Depends(get_db),
                   current_admin: int = Depends(oauth2.get_current_admin),
                   limit: Optional[int]=100, skip: Optional[int]=0,
                   search: Optional[str]= ""): #search filter by alert title

    history = db.query(models.History).filter(models.History.title.contains(search)).limit(limit).offset(skip).all()

    return history



# Get activity history by alert ID endpoint

@router.get('/{id}',response_model=List[schemas.HistoryOut])

def get_history_by_alert_id(id:int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    history= db.query(models.History).filter(models.History.alert_id==id).all()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"History with alert id: {id} does not exist")
    return history




# Get specific admin activity history by ID endpoint

@router.get('/admin/{id}',response_model=List[schemas.HistoryOut])

def get_activity_history_of_admin_by_admin_id(id:int,db: Session = Depends(get_db),current_admin: int = Depends(oauth2.get_current_admin)):

    history= db.query(models.History).filter(models.History.admin_id==id).all()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"History of admin activity id: {id} does not exist")
    return history



