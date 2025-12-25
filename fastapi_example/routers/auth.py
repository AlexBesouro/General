from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app import schemas, utils, oauth2
from app.database import models


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.AccessToken)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm = Depends() will extract FORM DATA, Depends() is empty because we are not passing any additional arguments to it, its dependency from fastapi.security almost like Depends(OAuth2PasswordRequestForm)
    # LOGIN LOGIC

    user = db.query(models.UserAlchemy).filter(
        # OAuth2PasswordRequestForm has username instead of email and expexcts from from front a form data not json
        models.UserAlchemy.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # PASSWORD LOGIC
    if not utils.pass_verifying(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # TOKEN CREATION
    # json only supports basic types: uuid.UUID is a custom object, so you must convert it yourself.
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
