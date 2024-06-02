import json
import CloudFlare

with open("../key.json", "r") as key:
    loads = json.loads(key.read())
    cloudflare_token = loads["cloudflare_token"]
    cloudflare_account_id = loads["cloudflare_account_id"]
    cloudflare_namespace_id = loads["cloudflare_namespace_id"]

with open("../metadata.json", "r") as metadata:
    data = json.loads(metadata.read())

cf = CloudFlare.CloudFlare(token=cloudflare_token)

upload_data = {
    "metadata": [{"metadata": "metadata"}],
    "value": data
}
cf.accounts.storage.kv.namespaces.values.put(cloudflare_account_id, cloudflare_namespace_id, "metadata", data = upload_data)