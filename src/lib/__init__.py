import pymongo
import os
import ijson
import sys
import bookstack


def json_file():
    return open("/mnt/tower/media/paperless/media/backup/test.json")

# import paperless database export
# manifest_path = "/mnt/user/media/paperless/media/manifest.json"

def json_cursor(f):
    items = ijson.items(f, 'item')
    docs = (doc for doc in items \
            if doc['model'] == "documents.document" \
            if sys.getsizeof(doc['fields']['content']) < 16777216)
    return docs

db = pymongo.MongoClient("10.0.0.59", 27017).paperless.content


url = 'http://10.0.0.59:6875'
token = 'RVSO8xZXOjRYJntNYPRd3E9iT2qXm11C'
secret = 'qR5r2EyKT09ogz8VSolS12ispAV5QrT0'

api = bookstack.BookStack(url, token, secret)
methods = api.generate_api_methods()