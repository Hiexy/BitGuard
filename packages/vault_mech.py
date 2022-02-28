import hashlib
from bson.objectid import ObjectId

def vault(users, id, password):
    d = dict()
    myquery = dict()

    d['_id'] = ObjectId(id)
    
    myquery['_id'] = { '$eq' : d['_id']}
    
    user = users.find_one(myquery)
    
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(user['salt']), 100000)
    print(len(key.hex()))
    return
    