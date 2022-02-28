import os
import pyte
import pytest
import time
import pymongo

from guard.database.connect import connect_col

@pytest.mark.order(1)
def test_if_not_connected():
    os.system('sudo systemctl stop mongod')
    time.sleep(2)

    with pytest.raises(Exception, match='MongoDB is not running/installed. Install mongodb or start it'):
        connect_col('test')

@pytest.mark.order(2)
def test_if_connected():
    os.system('sudo systemctl start mongod')
    time.sleep(2)
    test = connect_col('test')

    assert isinstance(test, pymongo.collection.Collection)

