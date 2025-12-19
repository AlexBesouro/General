from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
import psycopg
from psycopg.rows import class_row
from pydantic import BaseModel


# app = FastAPI()  # Better use FastAPI name for the app instance by convention but it's not mandatory


def get_conn():  # Function to establish a connection to the PostgreSQL database with psycopg
    try:
        return psycopg.connect(dbname="fastapi_example",
                               user="postgres",
                               password="password",
                               host="localhost",
                               port=5432)

    except Exception as e:
        print("Connection failed")
        print("Error: ", e)


class Thought(BaseModel):  # Pydantic model to validate and serialize thought data
    title: str
    content: str
    raiting: Optional[int] = None
    published: bool = False
    created_at: Optional[datetime] = None


# GET
# _-----------------------------------------------------------------------------------------------------------------------------------
@app.get("/thoughts")
async def get_thoughts():
    # row_factory=class_row(Thought) - converted into an instance of Thought, can now access columns as attributes, not by index
    # context manager to handle connection and cursor
    with get_conn() as conn, conn.cursor(row_factory=class_row(Thought)) as cur:
        all_thoughts = cur.execute(
            """SELECT * FROM thoughts""").fetchall()  # fetchall() returns a list of tuples by default
    # for t in all_thoughts: # ---- IN CASE IF IT TABLE VARIABLES ARE WITH DEFINED SIZE (CHAR(50))
    # # Better fix SQL tables
    #     t.title = t.title.rstrip()
    #     t.content = t.content.rstrip()
    return {"data": all_thoughts}


@app.get("/thoughts/{id}")
async def get_thought(id: int):
    with get_conn() as conn, conn.cursor(row_factory=class_row(Thought)) as cur:
        one_thought = cur.execute(
            """SELECT * FROM thoughts WHERE id = %s""", (id,)).fetchone()  # fetchone() returns a tuple by default:
        # psycopg expects a sequence (tuple/list) or mapping (dict), For a single parameter, you must make it a tuple with a comma -- (id,)
    if not one_thought:
        raise HTTPException(
            status_code=404, detail=f"Thought with id {id} not found")
    return {"thought detail": f"this is the thought you thought - {one_thought}"}


# POST
# -----------------------------------------------------------------------------------------------------------------------------------
@app.post("/thoughts", status_code=201)
async def post_thoughts(new_thought: Thought):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO thoughts (title, content, raiting, published) VALUES (%s,%s,%s,%s) RETURNING *""",
                    (new_thought.title, new_thought.content, new_thought.raiting, new_thought.published))
        thought = cur.fetchone()
    return {"new_post": thought}


# DELETE
# -----------------------------------------------------------------------------------------------------------------------------------
@app.delete("/thoughts/{id}", status_code=204)
async def delete_thought(id: int):
    with get_conn() as conn, conn.cursor() as cur:
        del_thought = cur.execute(
            """DELETE FROM thoughts WHERE id = %s RETURNING *""", (id,)).fetchone()
    if del_thought == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Thought with id - {id} doesn't exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE
# -----------------------------------------------------------------------------------------------------------------------------------
@app.put("/thoughts/{id}")
async def update_thought(id: int, thought: Thought):
    with get_conn() as conn, conn.cursor(row_factory=class_row(Thought)) as cur:
        updated_thought = cur.execute(
            """UPDATE thoughts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (thought.title, thought.content, thought.published, id)).fetchone()
    if updated_thought == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Thought with id - {id} doesn't exist")
    return {"message": updated_thought}
