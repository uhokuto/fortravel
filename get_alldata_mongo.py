
import csv
import urllib.request
import urllib.parse
import urllib
import lxml.html
import time
import pymongo
import pprint

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["fortravelDB2024"]
reviews_collection = db['fortravel_reviews']


count=0
for data in reviews_collection.find(no_cursor_timeout=True):
    pprint.pprint(data)
    count+=1
    print(count)
    #newvalues = { "$set": { "pref": "京都" } }
    #reviews_collection.update_one(data, newvalues)
 
    
    