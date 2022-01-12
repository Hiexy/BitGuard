#!/usr/bin/python3

from getpass import getpass
import os
import hashlib

def register(users):
    d = dict()
    myquery = dict()
    flag = False
    d['username'] = input('Enter username: ').lower()

    myquery['username'] = { '$eq' : d['username']}
    
    user = users.find(myquery)
    for i in user:
        if i['username'] == d['username']:
            print('Account name already exists. Please choose a unique name!')
            flag = True
    if flag:
        return

    password1 = getpass('Enter password: ')
    password2 = getpass('Confirm password: ')
    if password1 != password2:
        print('Passwords do not match')
        return
    
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password1.encode('utf-8'), salt, 100000)

    d['salt'] = salt.hex()
    d['hash'] = key.hex()
    
    users.insert_one(d)
    print('Account successfully created.')

def login(users):
    d = dict()
    myquery = dict()
    d['username'] = input('Enter username: ').lower()
    d['password'] = getpass('Enter password: ')

    myquery['username'] = { '$eq' : d['username']}

    user = users.find(myquery)
    x = list(user)
    if len(x) == 0:
            print('Incorrect Username/Password.')
            return

    for i in x:
        if i['username'] == d['username']:
            key = hashlib.pbkdf2_hmac('sha256', d['password'].encode('utf-8'), bytes.fromhex(i['salt']), 100000)
            if key.hex() == i['hash']:
                print('Logged In')
            else:
                print('Incorrect Username/Password.')