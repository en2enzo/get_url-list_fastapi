from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import os
#from crawl4ai import AsyncWebCrawler
#
#from openai import OpenAI
#import json
#import time

#app = FastAPI()

token = os.environ['API_TOKEN']

api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

def verify_token(auth_header: str = Depends(api_key_header)):
    #if auth_header != "expected_token":
    if auth_header != token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication token",
        )


app = FastAPI(
    title="test-fastapi",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "hello",
            "description": "APIのテスト",
        },
    ],
    dependencies=[Depends(verify_token)],
)


@app.get("/")
async def get_hello():
    return {"message": "Hello World5"}
