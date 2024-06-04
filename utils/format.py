import json

def format_json(loaded_data):
    metadata = []

    for item in loaded_data:
        if item["meta_pages"]:
            for page in item["meta_pages"]:
                temp_data = {
                    "id": item["id"],
                    "title": item["title"],
                    "tags": item["tags"],
                    "url": page["image_urls"]["original"],
                    "r18": item["x_restrict"],
                    "user": {
                        "account": item["user"]["account"],
                        "id": item["user"]["id"],
                        "name": item["user"]["name"],
                    }
                }
                metadata.append(temp_data)
        else:
            temp_data = {
                "id": item["id"],
                "title": item["title"],
                "tags": item["tags"],
                "url": item["meta_single_page"]["original_image_url"],
                "r18": item["x_restrict"],
                "user": {
                    "account": item["user"]["account"],
                    "id": item["user"]["id"],
                    "name": item["user"]["name"],
                }
            }
            metadata.append(temp_data)

    return metadata

if __name__ == "__main__":
    with open("../metadata.json", "r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    final_json = format_json(loaded_data)

    with open("testdata.json", 'w') as f:
        json.dump(final_json, f, indent=4)
