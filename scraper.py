from pixivpy3 import *
import json
from requests import *
from flask import jsonify

# Read secret
with open("key.json", "r") as key:
    key_loads = json.loads(key.read())
    key_refresh_token = key_loads["refresh_token"]
    key_illust = key_loads["user_bookmarks_illust"]

api = AppPixivAPI()
api.auth(refresh_token=key_refresh_token)
json_result = api.user_bookmarks_illust(key_illust)

merged_json = {}
merged_json.update(json_result)
merged_json = merged_json["illusts"]

# Get illust
while True:
	next_qs = api.parse_qs(json_result.next_url)
	json_result = api.user_bookmarks_illust(**next_qs)
	string_list = json_result["illusts"]
	merged_json.extend(string_list)
	print(next_qs)
	if api.user_bookmarks_illust(**next_qs).next_url == None :
		break

# Save into one JSON file
with open("metadata.json", "w") as file:
    json.dump(merged_json, file)