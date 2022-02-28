import pytest
import os
import time

CREDS = {
    'username': 'test',
    'password1': 'password',
    'password2': 'password'
}

from guard.auth.auth import register, login
from guard.database.connect import connect_col

@pytest.fixture
def col():
    return connect_col('test')

def test_register_used_username(col):
    col.delete_many({})
    register(col, **CREDS)
    with pytest.raises(Exception, match='Account name already exists. Please choose a unique name!'):
        register(col, **CREDS)

def test_register_mismatching_passwords(col):
    col.delete_many({})
    invalid_creds = CREDS.copy()
    invalid_creds['password2'] = 'invalid'
    with pytest.raises(Exception, match='Passwords do not match'):
        register(col, **invalid_creds)


def test_login_wrong_username(col):
    col.delete_many({})
    register(col, **CREDS)
    invalid_creds = CREDS.copy()
    invalid_creds['username'] = 'invalid'
    with pytest.raises(Exception, match='Incorrect Username/Password.'):
        login(col, invalid_creds['username'], invalid_creds['password1'])

def test_login_wrong_password(col):
    col.delete_many({})
    register(col, **CREDS)
    invalid_creds = CREDS.copy()
    invalid_creds['password1'] = 'invalid'
    with pytest.raises(Exception, match='Incorrect Username/Password.'):
        login(col, invalid_creds['username'], invalid_creds['password1'])


def test_login_successful(col):
    col.delete_many({})
    register(col, **CREDS)

    id, password = login(col, CREDS['username'], CREDS['password1'])

    assert password == CREDS['password1']

def test_registration_successful(col):
    col.delete_many({})

    msg = register(col, **CREDS)

    assert msg == 'Account successfully created.'
