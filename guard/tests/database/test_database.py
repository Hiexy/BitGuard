import os
import pytest
import time
import pymongo

from guard.database.connect import connect_col

@pytest.mark.order(1)
def test_if_not_connected():
    os.system('net stop MongoDB')

    with pytest.raises(Exception, match='MongoDB is not running/installed. Install mongodb or start it'):
        connect_col('test')

@pytest.mark.order(2)
def test_if_connected():
    os.system('net start MongoDB')
    test = connect_col('test')

    assert isinstance(test, pymongo.collection.Collection)

