import random
from typing import List, Optional
from fastapi import Body, Depends, FastAPI, Response, UploadFile, HTTPException, status
# this package is used to send files as responses
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import psycopg
from psycopg.rows import class_row
import time
from datetime import datetime, timezone
from .database.models import Base
from .database import models
from .database.db_connection import engine, get_db
from sqlalchemy.orm import Session
from . import schemas

app = FastAPI()  # Better use FastAPI name for the app instance by convention but it's not mandatory

Base.metadata.create_all(engine)


# @ is a decorator to define a route | .get is for GET requests | ("/") is the root path
# @app.get("/") sending a GET request to the local server (localgost:8000)
# async defines an asynchronous function/ asynchronous means it can handle multiple requests at the same time without blocking
# return sends a JSON response to a client (whoever makes the request to the server) with a message key and "Hello, World!" value


@app.get("/")
async def root():
    # FileRssponse is used to send files as responses
    return FileResponse('./images/johnsy.jpg')


# LIST is used to specify that the response will be a list of CreateThought models
@app.get("/thoughts", response_model=List[schemas.CreateThought])
# db is a session instance, Depends is used to inject dependencies into path operation functions, get_db is a function that provides a database session
def get_all_thoughts(db: Session = Depends(get_db)):
    # query is used to retrieve data from the database, all() returns all records from the ThoughtAlchemy table
    thoughts = db.query(models.ThoughtAlchemy).all()
    return thoughts


# response_model is used to specify the model that will be used to serialize the response data
@app.post("/thoughts", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateThought)
async def post_thoughts(thought: schemas.CreateThought, db: Session = Depends(get_db)):
    # new_thought = models.ThoughtAlchemy(title=thought.title, # ---- ALTERNATIVE WAY without unpacking
    #                                     content=thought.content)
    new_thought = models.ThoughtAlchemy(**thought.model_dump())
    # adding the new_thought instance to the database session, we need to use add every time we create a new instance
    db.add(new_thought)
    db.commit()  # committing the changes to the database
    # refreshing the instance to get the updated data from the database (like id)
    db.refresh(new_thought)
    return new_thought


@app.get("/thoughts/{id}")
def get_thought(id: int, db: Session = Depends(get_db), response_model=schemas.CreateThought):
    one_thought = db.query(models.ThoughtAlchemy).filter(  # filter is used to apply a condition to the query
        # first() returns the first record that matches the condition
        models.ThoughtAlchemy.id == id).first()
    if not one_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    return one_thought


@app.delete("/thoughts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_thought(id: int, db: Session = Depends(get_db)):
    one_thought = db.query(models.ThoughtAlchemy).filter(
        models.ThoughtAlchemy.id == id)
    if not one_thought.first():
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    one_thought.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/thoughts/{id}")
def update_thought(thought: schemas.UpdateThought, id: int, db: Session = Depends(get_db), response_model=schemas.CreateThought):
    # get() retrieves a record by its primary key or any other unique identifier
    updated_thought = db.get(models.ThoughtAlchemy, id)
    if not updated_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    for key, value in thought.model_dump().items():  # iterating over the key-value pairs of the thought model
        # setattr(obj, attr_name, value) -> one_thought, title, "Hello"  -> one_thought.title = "Hello", one_thought.content = "World"
        setattr(updated_thought, key, value)
    print(thought)
    # one_thought.update(thought.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(updated_thought)
    return updated_thought
