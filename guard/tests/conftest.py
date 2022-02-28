import time
import os

def pytest_configure(config):
    os.system('sudo systemctl start mongod')
    time.sleep(3)

def pytest_unconfigure(config):
    os.system('sudo systemctl stop mongod')