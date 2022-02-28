#!/usr/bin/python3

import os
import hashlib

def register(users, username, password1, password2):
    d = dict()
    myquery = dict()
    flag = False
    d['username'] = username

    myquery['username'] = { '$eq' : d['username']}
    
    user = users.find(myquery)
    for i in user:
        if i['username'] == d['username']:
            flag = True
    if flag:
        raise Exception('Account name already exists. Please choose a unique name!')

    if password1 != password2:
        raise Exception('Passwords do not match')
        
    
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password1.encode('utf-8'), salt, 100000)

    d['token'] = salt.hex() + key.hex()
    d['salt'] = os.urandom(32).hex()

    users.insert_one(d)
    return 'Account successfully created.'

def login(users, username, password):
    d = dict()
    myquery = dict()
    d['username'] = username
    d['password'] = password

    myquery['username'] = { '$eq' : d['username']}

    user = users.find(myquery)
    x = list(user)
    if len(x) == 0:
        raise Exception('Incorrect Username/Password.')

    for i in x:
        if i['username'] == d['username']:
            key = hashlib.pbkdf2_hmac('sha256', d['password'].encode('utf-8'), bytes.fromhex(i['token'][:64]), 100000)
            if key.hex() == i['token'][64:]:
                print('Logged In')
                return i['_id'], d['password']
            else:
                raise Exception('Incorrect Username/Password.')