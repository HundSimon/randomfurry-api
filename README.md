# randomfurry-api

做着玩的

## 调用

api 请求地址 GET `https://api.melaton.top/randomfurry/`

metadata 地址 `https://static.melaton.top/randomfurry/metadata.json`

Parameters:

- format 
  - json (默认) 返回 json 格式
  - image 302到图片地址
- r18
  - 0 (默认) 返回 SFW 的数据
  - 1 返回 NSFW 的数据

示例 API 每3天更新一次数据

## 部署

### 本地部署

1. 拉取仓库 `git clone https://github.com/HundSimon/randomfurry-api.git && cd randomfurry-api`

2. 获取 refresh token `python3 pixiv_auth.py`

3. 填写 pixiv 账户和 refresh token `cp key.json.example key.json`  `vim key.json`

4. 手动获取 metadata: `python3 scraper.py`

5. (可选) gunicorn 部署 `gunicorn app:randomfurry-api -c gunicorn_config.py --reload`

### Cloudflare Workers

1. 创建 worker，复制 `worker/worker.js` 的代码

2. 填写 `keyLoads` 的内容并部署

3. 创建 kv，键名 `metadata`，worker 命名空间绑定 `CLOUDFLARE_KV_NAMESPACE` 到刚刚创建的 kv

4. 更新 kv
   
   - (手动) 从`https://static.melaton.top/randomfurry/metadata.json` 获取 metadata并手动填写到 kv
   
   - (自动) 填写 `key.json` 的内容并运行 `scraper.py` , `worker/kv.py` 脚本进行更新

## Credit

- pixivpy [Pixiv API for Python · GitHub](https://github.com/upbit/pixivpy)
