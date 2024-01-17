from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List, Optional
from ..database import get_db

from ..googlemaps.maps import get_google_maps_link, get_current_location,set_location


router=APIRouter(
    prefix="/alerts",
    tags=['Alerts']
)


@router.get("/",response_model=List[schemas.PostResponse])
def get_alerts(db: Session = Depends(get_db),
               current_admin: Optional[models.Admin] = Depends(oauth2.get_admin),
               current_user: Optional[models.User] = Depends(oauth2.get_user),
               limit: Optional[int]=100, skip: Optional[int]=0,
               search: Optional[str]= ""): #search filter by title of alert

    if current_admin:
        #admin have the access to all the alerts
        # Fetch posts for admins
        alerts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    elif current_user:
        #user have the access only to his own alerts to view
        # Fetch posts for regular users
        alerts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return alerts



@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_alert(post:schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute(""" INSERT INTO alerts (title, content, location, published) VALUES (%s, %s, %s, %s) RETURNING * """,(post.title, post.content, 
    #post.location, post.published))
    #new_alert=cursor.fetchone()
    #conn.commit()
    #print(**post.dict()) unpack dictionnary
    #print(current_user.id)
    
    # Call the set_location function to set the location and location link
    post.location, post.location_link = set_location(post.location, post.location_link)

    new_alert = models.Post(owner_id=current_user.id, owner_phone_number=current_user.phone_number, **post.dict()) 

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert) #retrieve the new_alert and store it into the new variable new_alert
    return new_alert



@router.get("/{id}",response_model=schemas.PostResponse)
def get_alert(id: int,db: Session = Depends(get_db),
              current_admin: Optional[models.Admin] = Depends(oauth2.get_admin),
              current_user: Optional[models.User] = Depends(oauth2.get_user)):
    
    # cursor.execute("""SELECT * FROM alerts WHERE id=%s""",(str(id),))
    # alert=cursor.fetchone()

    alert=db.query(models.Post).filter(models.Post.id==id).first()
    #print(alert)

    if not alert:
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if current_user:
        if alert.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return alert



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alert(id: int,db: Session = Depends(get_db),
                 current_admin: Optional[models.Admin] = Depends(oauth2.get_admin),
                 current_user: Optional[models.User] = Depends(oauth2.get_user)):

    # cursor.execute("""DELETE FROM alerts WHERE id=%s RETURNING * """,(str(id),))
    # deleted_alert=cursor.fetchone()
    # conn.commit()

    alert_query=db.query(models.Post).filter(models.Post.id==id)

    alert=alert_query.first()

    if alert==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if current_user:
        if alert.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # if alert.owner_id!=current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    alert_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.PostResponse)
def update_alert(id:int, post:schemas.PostCreate,db: Session = Depends(get_db),
                 current_admin: Optional[models.Admin] = Depends(oauth2.get_admin),
                 current_user: Optional[models.User] = Depends(oauth2.get_user)):

    # cursor.execute("""UPDATE alerts SET title=%s, content=%s, location=%s, published=%s WHERE id=%s RETURNING * """,(post.title, post.content, 
    # post.location, post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()

    alert_query=db.query(models.Post).filter(models.Post.id==id)
    alert=alert_query.first()

    if alert==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if current_user:
        if alert.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # Call the set_location function to set the location and location link
    post.location, post.location_link = set_location(post.location, post.location_link)

    alert_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return alert_query.first()