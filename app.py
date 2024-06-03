from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import json
import random
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")

with open("metadata.json", "r") as file:
    loaded_data = json.load(file)

with open("key.json", "r") as key:
    key_loads = json.loads(key.read())
    key_refresh_token = key_loads["refresh_token"]
    key_illust = key_loads["user_bookmarks_illust"]
    key_proxy_url = key_loads["proxy_url"]

@app.get('/')
async def get_img(request: Request):
    # Args
    api_format = request.query_params.get("format")
    api_nsfw = request.query_params.get("r18", default = "0")

    # Get random data
    random_data = loaded_data[random.randint(0,len(loaded_data) - 1)]

    image_url_proxy = re.sub(r'i\.pximg\.net', key_proxy_url, random_data["url"])

    data = {
            "data" : {
                "id": random_data["id"],
                "title": random_data["title"],
                "tags": random_data["tags"],
                "url": random_data["url"],
                "proxy_url": image_url_proxy,
                "r18": random_data["r18"],
                "user": random_data["user"]
                },
            "code": 200
            }

    # Filter r18 tag
    if api_nsfw == "0" and random_data["r18"] == 1:
        return await get_img(request)
    if api_nsfw == "1" and random_data["r18"] == 0:
        return await get_img(request)

    # Return different formats
    if api_format == "image":
        return RedirectResponse(url=image_url_proxy)
    else:
        return JSONResponse(content=data)

@app.get('/index')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/index18')
async def index(request: Request):
    return templates.TemplateResponse("index18.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
