from uuid import UUID
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import models
from sqlalchemy.orm import Session
from app import schemas, utils
from app.database.db_connection import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = utils.hashing(user.password)
    new_user = models.UserAlchemy(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.CreateUserResponse)
def get_user(id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.UserAlchemy).filter(
        models.UserAlchemy.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} doesn't exist")
    return user
