from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
 
from .config import settings

#SQLALCHEMY_DATABASE_URL='postgresql://<username>:<password>@<ip-adress/hostname>/<database_name>'
#SQLALCHEMY_DATABASE_URL='postgresql://postgres:motdepasse@localhost:5432/projectDB'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database="projectDB",user="postgres",password="motdepasse",cursor_factory=RealDictCursor)
#         cursor= conn.cursor()
#         print("database connection was successfull!")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error:",error)
#         time.sleep(2)