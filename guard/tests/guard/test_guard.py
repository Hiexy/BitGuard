import os
import time

from guard.guard import Guard

def test_guard():
    os.system('sudo systemctl start mongod')
    time.sleep(5)
    guard = Guard()

    assert isinstance(guard, Guard)
