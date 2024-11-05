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
from routers import *
from core.config import settings





@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialization (Create resources, open connections, etc.)
 
    yield

    # Finalization (Delete resources, close connections, etc.)

    
   



tags_metadata = [
    {
        "name": "vectorstores",
        "description": "These Endpoints for make operations on vectorstores, by add or remove documents from it", 
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
    contact={"name": "GenAI", "url": "https://genai.ai", 'email': "qutaiba@sight.dev"}, 
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
)




# CORS
origins = [
    settings.BACKEND_URL, # backend
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



# app.include_router(
#     vectorstores.router,
#     prefix="/vectorstores",
#     tags=["vectorstores"],
#     dependencies=[],
# )



@app.get("/")
async def root():
    return RedirectResponse(url="/docs")













  
