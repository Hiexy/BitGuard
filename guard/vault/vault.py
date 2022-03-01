import hashlib
import time
import os
from bson.objectid import ObjectId

class Vault():
    def __init__(self, col, id, password):
        self.col = col
        self.vault = dict()
        self.id = id
        self.username = self.get_username()
        self.key = self.get_key(password)
    
    def get_key(self, password):
        d = dict()
        myquery = dict()

        d['_id'] = ObjectId(self.id)
        
        myquery['_id'] = { '$eq' : d['_id']}

        user = self.col.find_one(myquery)
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(user['salt']), 100000)
    
    def get_username(self):
        d = dict()
        myquery = dict()

        d['_id'] = ObjectId(self.id)
        
        myquery['_id'] = { '$eq' : d['_id']}

        user = self.col.find_one(myquery)
        return user['username']

    def add_item(self):
        name = input('Enter the name of the item: ')


def vault_interface(guard):
    time.sleep(3)
    os.system('clear')
    while True:
        print('Welcome username')
        input()

def main():
    pass


if __name__ == '__main__':
    main()