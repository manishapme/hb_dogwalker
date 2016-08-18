import unittest

import controller
# from controller import app
from model import db, connect_to_db
from seed_testdata import (populate_business, populate_users, populate_animals,
                           populate_people, populate_services, 
                           populate_reservations)

# write tests as we go
class ControllerTests(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = controller.app.test_client()

        # Show Flask errors that happen during tests
        controller.app.config['TESTING'] = True

        # Connect to test database
        # @todo set from environment config
        connect_to_db(controller.app, 'postgresql:///dogwalker')

        # # Create tables and add sample data
        db.drop_all()
        db.create_all()

        # # Populate the test data
        populate_business()
        populate_users()
        populate_animals()
        populate_people()
        populate_services()
        populate_reservations()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_sees_homepage(self):
        """Confirm user sees login button."""

        result = self.client.get('/')

        self.assertIn('Log Me In', result.data)
        self.assertNotIn('Logout', result.data)


    def test_login(self):
        """Confirm user can log in."""

        result = self.client.post('/login', 
                                  data={'user_name': 'mary',
                                        'password': '1234'},
                                  follow_redirects=True)
        self.assertIn('Logout', result.data)
        self.assertNotIn('Log Me In', result.data)

    def test_logout(self):
        """Confirm user can logout."""

        result = self.client.post('/login', 
                                  data={'user_name': 'mary',
                                        'password': '1234'},
                                  follow_redirects=True)

        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn('Log Me In', result.data)
        self.assertNotIn('Logout', result.data)

    def test_register_no_bizname(self):
        """Confirm user can register without adding business name."""

        result = self.client.post('/register', 
                                  data={'register_user_name': 'frank',
                                        'register_password': '1234',
                                        'register_first_name': 'frank',
                                        'register_last_name': 'franklast',
                                        'register_email': 'frank@frank',
                                        'register_business_name': ''},
                                  follow_redirects=True)

        self.assertIn('Add Business Details', result.data)


    def test_register_duplicate_username(self):
        """Confirm user is unable to register duplicate username."""

        result = self.client.post('/register', 
                                  data={'register_user_name': 'mary',
                                        'register_password': '1234',
                                        'register_first_name': 'frank',
                                        'register_last_name': 'franklast',
                                        'register_email': 'frank@frank',
                                        'register_business_name': ''},
                                  follow_redirects=True)
        
        self.assertIn('Please select another username.', result.data)


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
# adding a service
# person telephone number longer than 10 isn't allowed
# add a reservation
# edit a reservation

# @todo -- how to control what data a user can view


if __name__ == "__main__":
    unittest.main()
