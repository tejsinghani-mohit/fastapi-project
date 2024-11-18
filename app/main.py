from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root Path
@app.get("/", include_in_schema=False)
def read_root():
    return {"Hello": "World"}

#Routers
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
