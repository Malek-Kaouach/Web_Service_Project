from passlib.context import CryptContext

#what is the defualt hashing algorythm?
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashing the password
def hash(password: str):
    return pwd_context.hash(password)

#verify if the password inserted is valid
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)