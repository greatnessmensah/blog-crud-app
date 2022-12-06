from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post_route, user_route, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(post_route.router)
app.include_router(user_route.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}