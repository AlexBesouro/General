from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas
from app.database import models
from app.database.db_connection import get_db
from sqlalchemy.orm import Session

# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = "9f1c2a0c6d7f4b1e3c8a9d2e5f0a4b7c1d8e9a6f3b2c4e7d1a5c9b0f8e6"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRES_MINUTES = 1


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login")  # path from auth router

# Need to provide payload data - dict


def create_access_token(data: dict):
    data_to_encode = data.copy()  # Creating copy to not manipulate with original data
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCES_TOKEN_EXPIRES_MINUTES)
    # Addint extra property to encoding data to control expiration time -- "exp" inner jwt field to contol expiration time
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY,
                             algorithm=ALGORITHM)  # Creating a jwt
    return encoded_jwt
# This function will decode token and return user id from payload for protected routes


def verify_access_token(token: str, credential_exeptions):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Passing an argument from access_token = oauth2.create_access_token(data={"user_id": str(user.id)}) we used to add to payload to create token
        # Getting user id from payload to verify token
        user_id = decoded_jwt.get("user_id")
        if user_id is None:
            raise credential_exeptions
        # If id exists create TokenData schema object
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credential_exeptions
    # print(token_data, type(token_data))
    return token_data  # we returning an object of TokenData schema with id attribute
# This function will be used as a dependency in routes to get current user from token
# Dependency is a function (or class) that FastAPI runs for you before your endpoint, and whose result is automatically passed into your endpoint function.
# Endpoint = Route + Method + Function
# Depends will use oauth2_scheme to get the token from the request


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exeptions)
    user = db.query(models.UserAlchemy).filter(
        models.UserAlchemy.id == token.id).first()
    # print(user)
    return user
# Now you can use get_current_user as a dependency in any route to get the current user based on the token provided in the request.
