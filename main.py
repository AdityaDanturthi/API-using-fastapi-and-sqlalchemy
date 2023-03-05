from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

myPosts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "title of post 2", "content": "content of post 2", "id":2}]

@app.get("/")
def root():
    return {"Message": "Hello, world!"}


@app.post("/posts")
def create_posts(post: Post):
    print(post.dict())
    return {"Post details": post}



