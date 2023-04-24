import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobbers", "bob", "bob@gmail.com", "bobpass")
        assert user.username == "bob"

    def test_get_json(self):
        user = User(firstname="bob", lastname="bobbers", username="bob", email="bob@gmail.com", password="bobpass")
        user_json = user.get_json()
        expected_json = {
            'id': user.id,
            'firstname': 'bob',
            'lastname': 'bobbers',
            'username': 'bob',
            'email': 'bob@gmail.com',
        }
        self.assertDictEqual(user_json, expected_json)

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", "bobbers", "bob", "bob@gmail.com", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", "bobbers", "bob", "bob@gmail.com", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobbers", "bob", "bob@gmail.com", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("bob", "bobbers", "rick", "bob@gmail.com", "bobpass")
        assert user.username == "rick"


    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
