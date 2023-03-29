from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from app.db import *

app = FastAPI()

def randnum():
    return randint(1,10000)

def find_id(id):
     for i, p in enumerate(myPosts):
        if p["id"] == id:
            return i

while True:
    try:
        conn = psycopg2.connect(host= str(skey['host']), database= str(skey['database']), user= str(skey['user']), password = str(skey['password']), cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected to the database!')
        break
    except Exception as error:
        print('Connection to database failed!')
        print('Error:', error)
        time.sleep(2)

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "title of post 2", "content": "content of post 2", "id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/posts")
def root():
    cursor.execute("""SELECT * FROM posts""")
    posts =  cursor.fetchall()
    return {"posts": posts}

@app.get("/posts/{id}")
def getposts_id(id: int):
        id = str(id)
        cursor.execute("""SELECT * FROM posts WHERE id= (%s)""", (id))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} not found!" )
        return {"Post Details": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Post details": new_post}

@app.put("/posts/update/{id}")
def update_posts(id: int, updatedpost: Post):
    id = str(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s where id = %s RETURNING *""", (updatedpost.title, updatedpost.content, updatedpost.published, id))
    uppost = cursor.fetchone()
    conn.commit()
    if not uppost:
        err = str(status.HTTP_404_NOT_FOUND)
        return f"Error {err}: Post with id:{id} not found!"
    else:
        return {'Successfully updated the post!': uppost}        

@app.delete("/posts/delete/{id}", status_code= status.HTTP_202_ACCEPTED)
def delete_posts(id: int):
    id = str(id)
    cursor.execute("""DELETE FROM posts WHERE id= (%s) RETURNING *""",(id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        err = str(status.HTTP_404_NOT_FOUND)
        return f"Error {err}: Post with id:{id} not found!"
    else:
        return 'Successfully deleted the post!'


        