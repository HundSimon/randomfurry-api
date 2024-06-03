import json

def format_json(loaded_data):
    metadata = []

    for x in range(0, len(loaded_data) - 1):
        if loaded_data[x]["meta_pages"] == []:
            temp_data = {
                "id": loaded_data[x]["id"],
                "title": loaded_data[x]["title"],
                "tags": loaded_data[x]["tags"],
                "url": loaded_data[x]["meta_single_page"]["original_image_url"],
                "r18": loaded_data[x]["x_restrict"],
                "user": {
                    "account": loaded_data[x]["user"]["account"],
                    "id": loaded_data[x]["user"]["id"],
                    "name": loaded_data[x]["user"]["name"],
                }
            }
            metadata.append(temp_data)
        else:
            for y in range(0, len(loaded_data[x]["meta_pages"])): 
                temp_data = {
                    "id": loaded_data[x]["id"],
                    "title": loaded_data[x]["title"],
                    "tags": loaded_data[x]["tags"],
                    "url": loaded_data[x]["meta_pages"][y]["image_urls"]["original"],
                    "r18": loaded_data[x]["x_restrict"],
                    "user": {
                        "account": loaded_data[x]["user"]["account"],
                        "id": loaded_data[x]["user"]["id"],
                        "name": loaded_data[x]["user"]["name"],
                    }
                }
                metadata.append(temp_data)
    return metadata

if __name__ == "__main__":  
    with open("../metadata.json", "r", encoding="utf-8") as file:
        loaded_data = json.load(file)

    metadata = []

    final_json = format_json(loaded_data)

    with open("testdata.json", 'w') as f:
        json.dump(final_json, f, indent=4)