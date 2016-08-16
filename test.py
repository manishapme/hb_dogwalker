import unittest

from controller import app
from model import db, connect_to_db
from seed_testdata import (populate_business, populate_users, populate_animals,
                           populate_people)
import seed_testdata

# write tests as we go
class ControllerTests(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        # @todo set from environment config
        connect_to_db(app, "postgresql:///dogwalker")

        # Create tables and add sample data
        db.drop_all()
        db.create_all()

        # Populate the test data
        populate_business()
        populate_users()
        populate_animals()
        populate_people()


    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_login(self):
        """Confirm user can log in."""

        result = self.client.post('/login', 
                                  data={'user_name': 'mary',
                                        'password': '1234'},
                                  follow_redirects=True)
        self.assertNotIn('Login', result.data)


    def test_logout(self):
        """User is logged out"""

        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn('Login', result.data)

# user can register
# unauthorized user/pass cannot login
# unauthorized user cannot go to /business
# user can enter business name when registering and it exists in db
# user can create business separate from registration
# user can update business data
# clicking on edit enables all business form fields
# clicking on submit changes updates correct record in DB
# clicking on add new adds business correctly for current user
# adding a dog from business.html
# adding a person at same time you add a dog from business.html

# @todo -- how to control what data a user can view


if __name__ == "__main__":
    unittest.main()
