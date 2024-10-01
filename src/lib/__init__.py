import pymongo
import os
import json
import sys
import bookstack

db = pymongo.MongoClient("localhost", 27017).paperless.content


url = 'http://10.0.0.59:6875'
token = 'RVSO8xZXOjRYJntNYPRd3E9iT2qXm11C'
secret = 'qR5r2EyKT09ogz8VSolS12ispAV5QrT0'

api = bookstack.BookStack(url, token, secret)
methods = api.generate_api_methods()