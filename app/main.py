"""
Module Docstring
"""
import uvicorn
from fastapi import FastAPI

from app.routers import auth, posts, users, votes

##############################    Creatng FastAPI App   ##########################
app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)
