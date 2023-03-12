from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randint

app = FastAPI()

def randnum():
    return randint(1,10000)

def find_id(id):
     for i, p in enumerate(myPosts):
        if p["id"] == id:
            return i

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "title of post 2", "content": "content of post 2", "id":2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

@app.get("/posts")
def root():
    return {"posts": myPosts}

@app.get("/posts/{id}")
def getposts_id(id: int):
    for p in myPosts:
        if p["id"] == id:
            return p
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} not found!")

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    temp = randnum()
    post_dict = post.dict()
    post_dict["id"] = temp
    myPosts.append(post_dict)
    return {"Post details": post_dict}

@app.put("/posts/update/{id}")
def update_posts(id: int, updatedpost: Post):
    inx = find_id(id)
    if inx != None:
        updatedpost_dict = updatedpost.dict()
        print("before:", myPosts)
        updatedpost_dict["id"] = id
        myPosts[inx] = updatedpost_dict
        print("after:", myPosts)
        return f'Successfully updated the post!: {updatedpost}'
    else:
        err = str(status.HTTP_404_NOT_FOUND)
        return f"Error {err}: Post with id:{id} not found!"

@app.delete("/posts/delete/{id}", status_code= status.HTTP_202_ACCEPTED)
def delete_posts(id: int):
    inx = find_id(id)
    if inx == None:
        err = str(status.HTTP_404_NOT_FOUND)
        return f"Error {err}: Post with id:{id} not found!"
    else:
        myPosts.pop(inx)
        return 'Successfully deleted the post!'


        