from flask import Flask, jsonify, request, render_template, redirect
import json
import random
import re

app = Flask(__name__)

with open("metadata.json", "r") as file:
    loaded_data = json.load(file)

with open("key.json", "r") as key:
    key_loads = json.loads(key.read())
    key_refresh_token = key_loads["refresh_token"]
    key_illust = key_loads["user_bookmarks_illust"]
    key_proxy_url = key_loads["proxy_url"]

@app.route('/', methods=['GET'])
def get_img():
    # Args
    api_format = request.args.get("format")
    api_nsfw = request.args.get("r18", default = "0")

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
            }}

    # Filter r18 tag
    if api_nsfw == "0" and random_data["r18"] == 1:
        return get_img()
    if api_nsfw == "1" and random_data["r18"] == 0:
        return get_img()
    else:
        pass

    # Return different formats
    if api_format == "json":
        return jsonify(data)

    elif api_format == "image":
        return redirect(image_url_proxy, code=302)
    else:
        return jsonify(data)

@app.route('/index/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)