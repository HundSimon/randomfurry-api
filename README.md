# randomfurry-api

Returns furry images

做着玩的

## 调用

api 请求地址 GET `https://api.melaton.top/randomfurry/`

Parameters:

- format 
  - json (默认) 返回 json 格式
  - image 302到图片地址
- r18
  - 0 (默认) 返回 SFW 的数据
  - 1 返回 NSFW 的数据

示例 API 每3天更新一次数据

## 部署

1. 拉取仓库 `git clone https://github.com/HundSimon/randomfurry-api.git && cd randomfurry-api`

2. 获取 refresh token `python3 pixiv_auth.py`

3. 填写 pixiv 账户和 refresh token `cp key.json.example key.json`  `vim key.json`

4. 手动获取 metadata: `python3 scraper.py`

5. (可选) gunicorn 部署 `gunicorn app:randomfurry-api -c gunicorn_config.py --reload`

## Credit

- pixivpy [Pixiv API for Python · GitHub](https://github.com/upbit/pixivpy)


