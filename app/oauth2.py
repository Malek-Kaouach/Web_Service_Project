from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session 
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_KEY
#ALgorithm
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode=data.copy()
    
    expire= datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, id_key: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id = payload.get(id_key)
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise credentials_exception

    return token_data



""" 
def verify_access_token_4user(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id : str = payload.get("user_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    #error message when the token expires
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
         )

    except JWTError:
        raise credentials_exception
    
    return token_data


def verify_access_token_4admin(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id : str = payload.get("admin_id")
        print(id)
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))

    #error message when the token expires
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
         )

    except JWTError:
        raise credentials_exception
    
    return token_data
 """


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
        )
    
    #checking the token
    #print(token)

    id_key="user_id"
    token= verify_access_token(token, id_key ,credentials_exception)

    user= db.query(models.User).filter(models.User.id== token.id).first()

    return user



def get_current_admin(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
        )
    
    #checking the token
    #print(token)

    id_key="admin_id"
    token= verify_access_token(token, id_key ,credentials_exception)

    admin= db.query(models.Admin).filter(models.Admin.id== token.id).first()

    return admin



# get all alerts endpoint can get different output depending on the access token
# it uses a condition that accept either token from user or token from admin
# we should eliminate the 401 error in other to apply this condition
# that's why we will build 3 different functions to verify if we are dealing with user token or admin token

def verify_access_token_4alerts(token: str, id_key: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        id = payload.get(id_key)
        print(id)
        if id is None:
            return None
        token_data = schemas.TokenData(id=str(id))

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise credentials_exception

    return token_data



def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # checking the token
    # print(token)

    token = verify_access_token_4alerts(token, "user_id", credentials_exception)

    if token is None:
        return None  # Return None if token verification fails

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user



def get_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # checking the token
    # print(token)

    token = verify_access_token_4alerts(token, "admin_id", credentials_exception)

    if token is None:
        return None  # Return None if token verification fails

    admin = db.query(models.Admin).filter(models.Admin.id == token.id).first()

    return admin