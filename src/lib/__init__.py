import pymongo
import os
import ijson
import sys
import bookstack



# import paperless database export
# manifest_path = "/mnt/user/media/paperless/media/manifest.json"
f = open("/mnt/tower/media/paperless/media/backup/manifest.json")

manifest = ijson.items(f, 'item')

paperless_docs = {}

for doc in manifest:
    fields = doc['fields']
    if 'title' in fields and 'content' in fields:
        pk = doc['pk']
        title = fields['title']
        content = fields['content']
        check = fields['checksum']
        paperless_docs[pk] = {'checksum': check, 'title': title, 'content': content}


db = pymongo.MongoClient("10.0.0.59", 27017).paperless.content


url = 'http://10.0.0.59:6875'
token = 'RVSO8xZXOjRYJntNYPRd3E9iT2qXm11C'
secret = 'qR5r2EyKT09ogz8VSolS12ispAV5QrT0'

api = bookstack.BookStack(url, token, secret)
methods = api.generate_api_methods()