import hashlib
import time
import os
import random
import json
from base64 import b64encode, b64decode
from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from bson.objectid import ObjectId

class Vault():
    def __init__(self, col, id, password):
        self.col = col
        self.id = id
        self.vault = self.get_vault()
        self.username = self.get_username()
        self.key = self.get_key(password)
    
    def get_key(self, password):
        d = dict()
        myquery = dict()

        d['_id'] = ObjectId(self.id)
        
        myquery['_id'] = { '$eq' : d['_id']}

        user = self.col.find_one(myquery)
        return hashlib.md5(password.encode('utf-8') + bytes.fromhex(user['salt'])).digest()
    
    def get_username(self):
        d = dict()
        myquery = dict()

        d['_id'] = ObjectId(self.id)
        
        myquery['_id'] = { '$eq' : d['_id']}

        user = self.col.find_one(myquery)
        return user['username']

    def get_vault(self):
        d = dict()
        myquery = dict()

        d['_id'] = ObjectId(self.id)
        
        myquery['_id'] = { '$eq' : d['_id']}

        user = self.col.find_one(myquery)
        return user['vault']

    def add_item(self, guard):
        d = dict()
        name = input('Enter the name of the item: ')
        username = input('Enter username: ').encode()
        password = getpass('Enter password: ').encode()

        cipher = AES.new(self.key, AES.MODE_CBC)
        username_ct = cipher.encrypt(pad(username, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(username_ct).decode('utf-8')
        result = json.dumps({'iv':iv, 'ciphertext':ct})
        d['username'] = result

        cipher = AES.new(self.key, AES.MODE_CBC)
        password_ct = cipher.encrypt(pad(password, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(password_ct).decode('utf-8')
        result = json.dumps({'iv':iv, 'ciphertext':ct})
        d['password'] = result
        self.vault[name] = d
        filter = {'_id': self.id}
        newvalues = { '$set': {'vault': self.vault} }

        guard.col.update_one(filter, newvalues)

    def view_vault(self):
        for i in self.vault.keys():
            print(f'name:\t   {i}')
            b64 = self.vault[i]
            username = json.loads(b64['username'])
            iv = b64decode(username['iv'])
            ct = b64decode(username['ciphertext'])
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            print("username: ", pt.decode())

            password = json.loads(b64['password'])
            iv = b64decode(password['iv'])
            ct = b64decode(password['ciphertext'])
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            print("password: ", pt.decode())
            print()


    def __repr__(self):
        print(f'{self.col} {self.vault} {self.id} {self.username} {self.key}')

def vault_interface(guard):
    os.system('cls')
    for i in range(3):
        print('Logging in', end='')
        time.sleep(0.25)
        for j in range(5):
            time.sleep(0.25)
            print('.',end='')
        os.system('cls')
    
    
    time.sleep(2)
    welcome_string = f'Welcome {guard.vault.username} to your vault.'
    for i in welcome_string:
        print(i,end='')
        r = random.uniform(0.1, 0.45)
        time.sleep(r)
    print()
    while True:
        print('Choose one of the following options:')
        print('[N]ew entry')
        print('[V]iew vault')
        print('[Q]uit')

        q = input('> ')

        if q.lower() == 'n':
            guard.vault.add_item(guard)
        
        elif q.lower() == 'v':
            guard.vault.view_vault()
        
        elif q.lower() == 'q':
            exit()
            
        else:
            print()

def main():
    pass


if __name__ == '__main__':
    main()