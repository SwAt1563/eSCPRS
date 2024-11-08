from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response, status, Form, File, UploadFile, HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import RedirectResponse, ORJSONResponse
from fastapi.encoders import jsonable_encoder
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Annotated, Any
from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from contextlib import asynccontextmanager


from core.dependencies import dependencies
from routers import chats
from core.config import settings


# imports for the MongoDB database connection
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from schemas.documents import Purchase
from seeds.purchases import seed_data


# TODO: the ai assassment need to answer questions not just this project, be carful

# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client.get_database(settings.MONGODB_DATABASE)

    # Initialize beanie with the Purchase document class
    await init_beanie(database=app.mongodb, document_models=[Purchase])

    # Check if the collection is empty, then seed it
    collection = app.mongodb["purchases"]
    count = await collection.count_documents({})
    
    # Seed the data if the collection is empty
    if count == 0:
        await seed_data() 

    print("MongoDB connected.")

# method to close the database connection
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")

    
   
# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)



tags_metadata = [
    {
        "name": "chats",
        "description": "Operations with chats.",
    },
]

description = """
# GenAI APIs

"""
app = FastAPI(
    lifespan=lifespan, 
    dependencies=dependencies, # global dependencies | not matter what this function return, just what he did with its dependencies
    default_response_class=ORJSONResponse,
    title="GenAI APIs", 
    description=description, 
    version="0.0.1", 
    openapi_tags=tags_metadata, 
    contact={"name": "GenAI", "url": "https://genai.ai", 'email': "qutaibaolayyan@gmail.com"}, 
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
)




# CORS
origins = [
    settings.FRONTEND_URL,
  
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static") # the static folder must be created


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    from time import time
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.include_router(
    chats.router,
    prefix="/chats",
    tags=["chats"],
    dependencies=[],
)



@app.get("/")
async def root():
    return RedirectResponse(url="/docs")













  
