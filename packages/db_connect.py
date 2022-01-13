#! /usr/bin/python3

import pymongo

def connectcol(collection):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    bg = myclient["bitguard"]
    col = bg[collection]
    return col