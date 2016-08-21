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


    def test_register_later_bizname(self):
        """Confirm user can register and seperately add business name."""

        result = self.client.post('/register', 
                                  data={'register_user_name': 'frank',
                                        'register_password': '1234',
                                        'register_first_name': 'frank',
                                        'register_last_name': 'franklast',
                                        'register_email': 'frank@frank',
                                        'register_business_name': ''},
                                  follow_redirects=True)
        self.assertIn('Add Business Details', result.data)

        result = self.client.post('/business/add', 
                                  data={'business_name': 'franksdogs',
                                        'street': '683 Sutter Street',
                                        'city': 'San Francisco',
                                        'state': 'CA',
                                        'zip': '94103',
                                        'phone': '4155555555',
                                        'url': 'franksurl',
                                        'license': 'frankslicense'},
                                  follow_redirects=True)

        self.assertIn('Edit Business Details', result.data)
        self.assertIn('franksdogs', result.data)
        self.assertIn('683 Sutter Street', result.data)
        self.assertIn('San Francisco', result.data)
        self.assertIn('CA', result.data)
        self.assertIn('94103', result.data)
        self.assertIn('4155555555', result.data)
        self.assertIn('franksurl', result.data)
        self.assertIn('frankslicense', result.data)


    def test_register(self):
        """User can register with a business name."""

        result = self.client.post('/register',
                                   data={'register_user_name': 'sally',
                                        'register_password': '1234',
                                        'register_first_name': 'Sally',
                                        'register_last_name': 'Sallylast',
                                        'register_email': 'sally@sally',
                                        'register_business_name': 'Sally\'s Pets'                                  
                                   },
                                   follow_redirects=True
                                   )
        self.assertIn('Sally&#39;s Pets', result.data)
        self.assertIn('Welcome Sally', result.data)
        self.assertIn('Edit Business Details', result.data)


    def test_business_update(self):
        """Confirm user can update business details."""

        result = self.client.post('/login', 
                                  data={'user_name': 'mary',
                                        'password': '1234'},
                                  follow_redirects=True)
        self.assertIn('Logout', result.data)
        self.assertNotIn('Log Me In', result.data)


        result = self.client.post('/business/update', 
                                  data={'business_name': 'franksdogs',
                                        'street': '683 Sutter Street',
                                        'city': 'San Francisco',
                                        'state': 'CA',
                                        'zip': '94103',
                                        'phone': '4155555555',
                                        'url': 'franksurl',
                                        'license': 'frankslicense'},
                                  follow_redirects=True)

        self.assertIn('Edit Business Details', result.data)
        self.assertIn('franksdogs', result.data)
        self.assertIn('683 Sutter Street', result.data)
        self.assertIn('San Francisco', result.data)
        self.assertIn('CA', result.data)
        self.assertIn('94103', result.data)
        self.assertIn('4155555555', result.data)
        self.assertIn('franksurl', result.data)
        self.assertIn('frankslicense', result.data)
        self.assertIn('disabled', result.data)


    def test_unauthorized_login(self):
        """Unauthorized user/pass cannot login."""

        result = self.client.post('/login',
                                  data={'user_name': 'mary',
                                        'password': '12345'},
                                  follow_redirects=True)
        self.assertIn('did not match a registered user', result.data)


    def test_route_blocked(self):
        """Unauthorized user/pass cannot view route requiring login."""

        result = self.client.get('/business', follow_redirects=True)

        self.assertIn('Unauthorized', result.data)

    def test_add_animal(self):
        """adding a person at same time you add a dog from business.html"""

        result = self.client.post('/login',
                                  data={'user_name': 'mary',
                                        'password': '1234'},
                                  follow_redirects=True)
        self.assertIn('Logout', result.data)
        self.assertNotIn('Log Me In', result.data)

        result = self.client.post('/animal/add',
                                   data={'business_id': '1',
                                        'name': 'Julius',
                                        'species': 'Dog',
                                        'breed': 'German Shepard',
                                        'birthday': '3/1/2005',
                                        'vet': 'Four Seasons Pet Hospital',
                                        'note': 'Needs muzzle on trail',
                                        'fullname': 'Sally Brown',
                                        'street': '200 Irving Street',
                                        'city': 'San Francisco',
                                        'state': 'CA',
                                        'zipcode': '94122',
                                        'phone': '3101111111',
                                        'email': 'sally@brown'                         
                                   },
                                   follow_redirects=True
                                   )
        self.assertIn('Julius', result.data)
        self.assertIn('Sally Brown', result.data)



# JAVASCRIPT clicking on edit enables all business form fields
# adding a dog from business.html
# adding a service
# person telephone number longer than 10 isn't allowed
# add a reservation
# edit a reservation

# @todo -- how to control what data a user can view


if __name__ == "__main__":
    unittest.main()
