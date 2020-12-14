import uvicorn
from fastapi import FastAPI

#from config import get_config
from app.db import db
from app.api import posts

app = FastAPI()

app.include_router(posts.router, prefix='/api')


@app.on_event("startup")
async def startup():
    await db.connect_to_database()


@app.on_event("shutdown")
async def shutdown():
    await db.close_database_connection()


if __name__ == "__main__":
    uvicorn.run(app)