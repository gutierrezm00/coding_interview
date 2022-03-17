
from availability import *

def test_filterUsers():
    query_users = ['Jane', 'John', 'Maggie']
    users = [{'id': 1, 'name': 'Jane'}, {'id': 2, 'name': 'John'}, {'id': 3, 'name': 'Maggie'}, {'id': 4, 'name': 'Nick'}, {'id': 5, 'name': 'Emily'}, {'id': 6, 'name': 'Joe'}, {'id': 7, 'name': 'Jordan'}]
    assert filterUsers(query_users,users) == [{'id': 1, 'name': 'Jane'}, {'id': 2, 'name': 'John'}, {'id': 3, 'name': 'Maggie'}]
