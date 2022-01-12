from getpass import getpass
import pymongo
import os
import hashlib

banner = '''
██████╗ ██╗████████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ 
██╔══██╗██║╚══██╔══╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
██████╔╝██║   ██║   ██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██╔══██╗██║   ██║   ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║   ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝


'''

def main():
    print(banner)
    print('Welcome To BitGuard')
    print('\n' * 10)
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    bg = myclient["bitguard"]
    users = bg["users"]

    while True:
        print('\n' * 5)
        print('Choose one of the following options:')
        print('[L]ogin')
        print('[R]egister a new account')
        print('[D]elete all accounts.')
        print('[V]iew all acounts.')
        print('[Q]uit.')
        query = input("> ")
        
        if query.lower() == 'l':
            d = dict()
            myquery = dict()
            d['username'] = input('Enter username: ').lower()
            d['password'] = getpass('Enter password: ')

            myquery['username'] = { '$eq' : d['username']}

            user = users.find(myquery)
            x = list(user)
            if len(x) == 0:
                    print('Incorrect Username/Password.')
                    continue
            for i in x:
                if i['username'] == d['username']:
                    key = hashlib.pbkdf2_hmac('sha256', d['password'].encode('utf-8'), bytes.fromhex(i['salt']), 100000)
                    if key.hex() == i['hash']:
                        print('Logged In')
                    else:
                        print('Incorrect Username/Password.')
                    

        elif query.lower() == 'r':
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
                continue

            password1 = getpass('Enter password: ')
            password2 = getpass('Confirm password: ')
            if password1 != password2:
                print('Passwords do not match')
                continue
            
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password1.encode('utf-8'), salt, 100000)

            d['salt'] = salt.hex()
            d['hash'] = key.hex()
            
            users.insert_one(d)
            print('Account successfully created.')

        elif query.lower() == 'd':
            users.delete_many({})

        elif query.lower() == 'v':
            for x in users.find():
                print(x)

        elif query.lower() == 'q':
            exit()

        else:
            print('Error, incorrect option.')







if __name__ == "__main__":
    main()