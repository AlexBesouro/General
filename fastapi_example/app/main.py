from fastapi import FastAPI
from fastapi.responses import FileResponse
from .database.models import Base
from .database.db_connection import engine
from routers import thoughts, users, auth


app = FastAPI()  # Better use FastAPI name for the app instance by convention but it's not mandatory

app.include_router(thoughts.router)
app.include_router(users.router)
app.include_router(auth.router)


Base.metadata.create_all(engine)


# @ is a decorator to define a route | .get is for GET requests | ("/") is the root path
# @app.get("/") sending a GET request to the local server (localgost:8000)
# async defines an asynchronous function/ asynchronous means it can handle multiple requests at the same time without blocking
# return sends a JSON response to a client (whoever makes the request to the server) with a message key and "Hello, World!" value


@app.get("/")
async def root():
    # FileRssponse is used to send files as responses
    return FileResponse('./images/johnsy.jpg')
