from getpass import getpass

from guard.database.connect import connect_col
from guard.auth.auth import register, login
from guard.vault.vault import Vault, vault_interface

class Guard():
    def __init__(self):
        self.col = connect_col('users')
    
    def register(self):
        username = input('Enter username: ').lower()
        password1 = getpass('Enter password: ')
        password2 = getpass('Confirm password: ')
        return register(self.col, username, password1, password2)
    
    def login(self):
        username = input('Enter username: ').lower()
        password = getpass('Enter password: ')
        id, masterKey = login(self.col, username, password)
        self.vault = Vault(self.col, id, masterKey)
    
    def delete_all(self):
        self.col.delete_many({})


def interface():
    try:
        guard = Guard()
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
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
                if masterKey:
                    guard.init_vault(guard.col, id, masterKey)
                    vault_interface(guard)
                else:
                    print(id)
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

def main():
    guard = Guard()
    guard.login()

    print(guard.vault.username)

if __name__=='__main__':
    main()