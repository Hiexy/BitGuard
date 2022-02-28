#! /usr/bin/python3

import pymongo

from guard.config import MAXSEVDELAY

def connect_col(collection):
    try:
        myclient = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=MAXSEVDELAY)
        myclient.server_info()
        bg = myclient["bitguard"]
        col = bg[collection]
        return col
    except pymongo.errors.ServerSelectionTimeoutError as err:
        raise Exception("MongoDB is not running/installed. Install mongodb or start it.")
        
    