import time
import os

def pytest_configure(config):
    os.system('net start MongoDB')

def pytest_unconfigure(config):
    os.system('net stop MongoDB')