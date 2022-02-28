#! /usr/bin/python3

import bson
from guard.guard import Guard

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
    print('\n' * 5)

    guard = Guard()
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
            try:
                id, masterKey = guard.login()
                print(id, masterKey)
                # if masterKey:
                #     vault(users, id, masterKey)
                # else:
                #     print(id)
            except Exception as e:
                print(f'Error: {e}')
                    
        elif query.lower() == 'r':
            try:
                print(guard.register())
            except Exception as e:
                print(f'Error: {e}')

        elif query.lower() == 'd':
            try:
                guard.delete_all()
            except Exception as e:
                print(f'Error: {e}')
            
        elif query.lower() == 'v':
            for x in guard.col.find():
                print(x)

        elif query.lower() == 'q':
            exit()

        else:
            print('Error, incorrect option.')

if __name__ == "__main__":
    main()