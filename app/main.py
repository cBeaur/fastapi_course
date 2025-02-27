from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from . routers import post, user


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host='localhost', dbname='fastapi', user='postgres', password='1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected to the database successfully.')
        break
    except Exception as error:
        print('Connection to the database failed.')
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id": 2}]


def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
