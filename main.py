#! /usr/bin/python3

from packages.auth_mech import login, register
from packages.db_connect import connectcol

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

    users = connectcol('users')

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
            ans = login(users)
            print(ans)
                    
        elif query.lower() == 'r':
            print(register(users))

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