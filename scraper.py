from pixivpy3 import *
import json
from requests import *
from flask import jsonify

# Read secret
with open("key.json", "r") as key:
    key_loads = json.loads(key.read())
    key_refresh_token = key_loads["refresh_token"]
    key_illust = key_loads["user_bookmarks_illust"]

# Initialize
api = AppPixivAPI()
api.auth(refresh_token=key_refresh_token)

# Remove duplicated
def remove_duplicates(json_data):
    string_data = [json.dumps(d, sort_keys=True) for d in json_data]
    string_data = list(dict.fromkeys(string_data))
    json_data = [json.loads(s) for s in string_data]
    return json_data

def append_json(file_path, new_data):
    with open(file_path, 'r') as f:
        existing_data = json.load(f)
    existing_data.extend(new_data)
    existing_data = remove_duplicates(existing_data)
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

def remove_dicts_without_tags(file_path, tag_names):
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    filtered_data = [d for d in json_data if any(any(tag['name'] == tag_name or tag['translated_name'] == tag_name for tag in d.get('tags', [])) for tag_name in tag_names)]
    with open(file_path, 'w') as f:
        json.dump(filtered_data, f, indent=4)

# Get Metadatas
def get_bookmark_illusts():
	merged_json = {}
	json_result = api.user_bookmarks_illust(key_illust)
	merged_json.update(json_result)
	merged_json = merged_json["illusts"]

	while True:
		next_qs = api.parse_qs(json_result.next_url)
		json_result = api.user_bookmarks_illust(**next_qs)
		string_list = json_result["illusts"]
		merged_json.extend(string_list)
		print(next_qs)
		if api.user_bookmarks_illust(**next_qs).next_url == None :
			return merged_json

def get_followed_illusts():
	merged_json = {}
	json_result = api.illust_follow(req_auth=True)
	merged_json.update(json_result)
	merged_json = merged_json["illusts"]

	for x in range(10):
	    next_qs = api.parse_qs(json_result.next_url)
	    json_result = api.illust_follow(**next_qs)
	    merged_json.extend(json_result.illusts)
	    print(api.illust_follow(**next_qs).next_url)
	return merged_json

# Save into one JSON file
append_json("metadata.json", get_bookmark_illusts())
append_json("metadata.json", get_followed_illusts())

# Remove irrelevant tagged contents
tag_names = ["furry", "furry shota", "furry male", "beast", "Arknights"]
remove_dicts_without_tags("metadata.json", tag_names)