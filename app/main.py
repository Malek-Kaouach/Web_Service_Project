from fastapi import FastAPI
from . import models
from .database import engine
from .routers import alert,user,auth,admin,history,ban
from .config import settings

models.Base.metadata.create_all(bind=engine)


# Create tags names and description 
tags_metadata = [
    {
        "name": "Authentication",
        "description": "API endpoints for user authentication"
    },
    {
        "name": "Alerts",
        "description": "API endpoints for managing alerts"
    },
    {
        "name": "Users",
        "description": "API endpoints for managing user data"
    },
    {
        "name": "Admins",
        "description": "API endpoints for administrative tasks"
    },
        {
        "name": "Banning System",
        "description": "API endpoints for managing banning system"
    }
    ,
    {
        "name": "Activity History",
        "description": "API endpoints for retrieving historical data (admins activity)"
    }
]


app = FastAPI(
    title="Accident Report API",
    description="Transportation API: Accident Assistance Support System \n\n Web Service Academic Project \n\n By: Mohamed Malek Kaouach",
    openapi_tags=tags_metadata,
)


app.include_router(auth.router, tags=["Authentication"])
app.include_router(alert.router, tags=["Alerts"])
app.include_router(user.router, tags=["Users"])
app.include_router(admin.router, tags=["Admins"])
app.include_router(ban.router, tags=["Banning System"])
app.include_router(history.router, tags=["Activity History"])






