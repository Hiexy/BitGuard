#! /usr/bin/python3

import pymongo

def connectcol(collection):
    maxSevSelDelay = 2
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=maxSevSelDelay)
        myclient.server_info()
        bg = myclient["bitguard"]
        col = bg[collection]
        return col
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("MongoDB is not running/installed. Install mongodb or start it.")
        exit(1)
    