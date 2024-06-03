from pixivpy3 import *
import json
from requests import *
from flask import jsonify
from utils.format import format_json

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

def get_recommended_illusts():
	merged_json = {}
	json_result = api.illust_recommended(content_type="illust")
	merged_json.update(json_result)
	merged_json = merged_json["illusts"]
	return merged_json


temp_metadata = []

with open("metadata.json", "r", encoding="utf-8") as old_metadata:
	final_metadata = json.load(old_metadata)
	temp_metadata.extend(get_bookmark_illusts())
	temp_metadata.extend(get_followed_illusts())
	temp_metadata.extend(get_recommended_illusts())
	final_metadata.extend(format_json(loaded_data=temp_metadata))

with open("metadata.json", 'w') as new_metadata:
    json.dump(final_metadata, new_metadata, indent=4)

# Remove irrelevant tagged contents
tag_names = ["furry", "furry shota", "furry male", "beast", "kemono", "獣人", "獸", "兽人", "ケモノ", "竜人", "オスケモ"]
remove_dicts_without_tags("metadata.json", tag_names)