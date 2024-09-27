import pymongo
import os
import json
import sys

db = pymongo.MongoClient("localhost", 27017).paperless.content
