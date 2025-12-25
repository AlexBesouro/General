from typing import List, Optional
from uuid import UUID
from fastapi import Depends, Response, HTTPException, status, APIRouter
from app.database import models
from app.database.db_connection import get_db
from sqlalchemy.orm import Session
from app import schemas, oauth2

router = APIRouter(prefix="/thoughts", tags=["Thoughts"])


@router.get("/", response_model=List[schemas.CreateThoughtResponse])
# LIST is used to specify that the response will be a list of CreateThought models
# db is a session instance, Depends is used to inject dependencies into path operation functions, get_db is a function that provides a database session
# When I use response_model i always need to make sure that the returned data matches the schema defined in the response_model, otherwise FastAPI will raise a validation error.
def get_all_thoughts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # query is used to retrieve data from the database, all() returns all records from the ThoughtAlchemy table
    # For limit query parametr we need to add limit() func
    # For skip query parametr we need to add offset() func
    # For search query parametr we need to use filter + contains() func
    thoughts = db.query(models.ThoughtAlchemy).filter(models.ThoughtAlchemy.title.contains(search)).limit(
        limit).offset(skip).all()
    print(limit)
    return thoughts


# response_model is used to specify the model that will be used to serialize the response data
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateThoughtResponse)
async def post_thoughts(thought: schemas.CreateThought, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    # new_thought = models.ThoughtAlchemy(title=thought.title, # ---- ALTERNATIVE WAY without unpacking
    #                                     content=thought.content)

    new_thought = models.ThoughtAlchemy(
        **thought.model_dump(), user_id=current_user.id)
    # adding the new_thought instance to the database session, we need to use add every time we create a new instance
    db.add(new_thought)
    db.commit()  # committing the changes to the database
    # refreshing the instance to get the updated data from the database (like id)
    db.refresh(new_thought)
    return new_thought


@router.get("/{id}")
def get_thought(id: UUID, db: Session = Depends(get_db), response_model=schemas.CreateThoughtResponse):
    one_thought = db.query(models.ThoughtAlchemy).filter(  # filter is used to apply a condition to the query
        # first() returns the first record that matches the condition
        models.ThoughtAlchemy.id == id).first()
    if not one_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    return one_thought


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_thought(id: UUID, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    one_thought_query = db.query(models.ThoughtAlchemy).filter(
        models.ThoughtAlchemy.id == id)
    one_thought = one_thought_query.first()
    if not one_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    if one_thought.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform request")
    one_thought_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_thought(thought: schemas.CreateThoughtResponse, id: UUID, db: Session = Depends(get_db),  current_user: str = Depends(oauth2.get_current_user), response_model=schemas.CreateThought):
    # get() retrieves a record by its primary key or any other unique identifier
    updated_thought_query = db.query(models.ThoughtAlchemy).filter(
        models.ThoughtAlchemy.id == id)
    updated_thought = updated_thought_query.first()
    if not updated_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    updated_thought_query.update(
        thought.model_dump(), synchronize_session=False)

    # for key, value in thought.model_dump().items():  # iterating over the key-value pairs of the thought model
    # setattr(obj, attr_name, value) -> one_thought, title, "Hello"  -> one_thought.title = "Hello", one_thought.content = "World"
    # setattr(updated_thought, key, value)
    # one_thought.update(thought.model_dump(), synchronize_session=False)

    db.commit()
    db.refresh(updated_thought)
    return updated_thought
