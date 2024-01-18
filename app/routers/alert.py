import datetime
from decimal import Decimal
from sqlalchemy import func
from geoalchemy2.types import Geography

from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session 
from typing import List, Optional
from ..database import get_db

from ..googlemaps.maps import set_location, get_coordinates, calculate_distance




router=APIRouter(
    prefix="/alerts",
    tags=['Alerts']
)



# Get all alerts endpoint

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



# Create alert endpoint

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



# Get alert by ID endpoint

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




@router.get("/inradius/{id}", response_model=List[schemas.NearestAlerts])
def get_alerts(
    id: int,
    db: Session = Depends(get_db),
    current_admin: int = Depends(oauth2.get_current_admin)
):
    # Get the admin location
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    admin_location = admin.location

    # Get the alert locations
    alerts = (db.query(models.Post).all())


    print('response radius = ',admin.response_radius)

    # List to store the IDs of alerts and distances
    alert_info = []

    for alert in alerts:
        # Get the latitude and longitude coordinates for the admin's location
        admin_loc = get_coordinates(admin_location)

        # Get the latitude and longitude coordinates for the alert's location
        alert_loc = get_coordinates(alert.location)

        if admin_loc is not None and alert_loc is not None:
            distance = calculate_distance(admin_loc, alert_loc)
            print(f"distance from alert [{alert.id}] is ",distance)
        else:
            print(f"distance from alert [{alert.id}] is None")

        # Convert admin.response_radius to a decimal
        response_radius = Decimal(admin.response_radius)

        if distance <= response_radius:
            alert_info.append({"id": alert.id, "distance": distance})

        
    print(alert_info)

    # Extract alert IDs for the nearest alerts
    alert_ids = [info["id"] for info in alert_info]

    # Retrieve the nearest alerts from the database
    nearest_alerts = db.query(models.Post).filter(models.Post.id.in_(alert_ids)).all()

    # Add the distance information to each alert
    for alert in nearest_alerts:
        alert.distance = next(info["distance"] for info in alert_info if info["id"] == alert.id)

    return nearest_alerts







# Delete alert by ID endpoint

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



# Update alert by ID endpoint

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



# Update status alert by ID endpoint

@router.put("/status/{id}",response_model=schemas.PostResponse)
def update_status(id: int, post:schemas.PostStatus, db: Session = Depends(get_db),
                  current_admin: int = Depends(oauth2.get_current_admin)):

    alert_query=db.query(models.Post).filter(models.Post.id==id)
    alert=alert_query.first()

    if alert==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    alert_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return alert_query.first()