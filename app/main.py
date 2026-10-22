from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routes import post,user,auth,vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)# here post is the file name and router is the APIRouter object created there
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message":"Hello World"}




