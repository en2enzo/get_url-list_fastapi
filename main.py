from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import os
from crawl4ai import AsyncWebCrawler

from openai import OpenAI
import json
import time

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


async def get_content_crawl(url):
#def get_urls_crawl(url):
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(
            url=url,
            verbose=False,
            headless=True
        )
        #return result.markdown
        #for item in result.links['internal']:
        #    print("--------bc-------------")
        #    print(item['text'],item['href'])
        #    print("##" + item['text'])

        ans = result.markdown

        return ans

async def get_urls_crawl(url):
#def get_urls_crawl(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(

            url=url
        )
        #return result.markdown
        #for item in result.links['internal']:
        #    print("--------bc-------------")
        #    print(item['text'],item['href'])
        #    print("##" + item['text'])
        print(type(result))
        ans = result.links['internal']
        list = []
        for item in ans:
            #print(item['text'],item['href'])
            list.append(item['href'])
        #ans = result.links['internal'][:3]
        #ans = result.links['internal'][:100]
        print(type(ans))

        #return ans
        return list
    #print("aaa")


####################
### Get
####################


@app.get("/")
async def get_hello():
    return {"message": "Hello World5"}

@app.get("/crawl")
async def crawl_url(url: str):
    try:
        content = await get_content_crawl(url)
        return {"content": content}
        #return url
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"クロール中にエラーが発生しました: {str(e)}"
        )

@app.get("/crawl_urls")
async def crawl_urls(url: str):
    try:
        urls = await get_urls_crawl(url)
        #return {"urls": urls}
        return urls
        #print(type(urls))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"クロール中にエラーが発生しました: {str(e)}"
        )


