from getpass import getpass

from guard.database.connect import connect_col
from guard.auth.auth import register, login
from guard.vault.vault import Vault

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
        return login(self.col, username, password)
    
    def delete_all(self):
        self.col.delete_many({})

    def init_vault(self, id, password):
        self.vault = Vault(self.col, id, password)

def main():
    guard = Guard()
    print(guard.register())
    print(guard.login())

if __name__=='__main__':
    main()