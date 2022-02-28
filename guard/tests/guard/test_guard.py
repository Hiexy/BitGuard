import os
import time

from guard.guard import Guard

def test_guard():
    guard = Guard()

    assert isinstance(guard, Guard)
