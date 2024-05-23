from flask import Flask, jsonify, request, render_template, redirect
import json
import random
import re

app = Flask(__name__)

with open("metadata.json", "r") as file:
    loaded_data = json.load(file)

@app.route('/', methods=['GET'])
def get_img():
    # Args
    api_format = request.args.get("format")
    api_proxy = request.args.get("proxy")

    random_data = loaded_data[random.randint(0,len(loaded_data) - 1)]
    image_url_proxy = re.sub(r'pximg\.net', 'pixiv.re', random_data["image_urls"]["large"])

    data = {
            "data" : {
                "id" : random_data["id"],
                "title" : random_data["title"],
                "image_url" : random_data["image_urls"]["large"],
                "image_url_proxy" : image_url_proxy,
                "user" : {
                    "name" : random_data["user"]["name"],
                    "id" : random_data["user"]["id"],
                    "account" : random_data["user"]["account"],
                },
                "tags" : random_data["tags"]
            },
            }

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