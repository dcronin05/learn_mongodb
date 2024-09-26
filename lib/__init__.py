import pymongo
import os
import json
import sys
import pprint

db = pymongo.MongoClient("localhost", 27017).paperless.content
