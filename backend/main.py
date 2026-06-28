from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import get_db, engine, Base
from routers import session_routes, ai_routes

Base.metadata.create_all(bind=engine) 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_routes.router)
# app.include_router(ai_routes.router)
