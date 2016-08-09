# populate test data
# @todo use separate db for tests
from model import User
from model import connect_to_db, db
from controller import app

def populate_users():
    """Create minimum sample data for the user table."""

    print "Users - begin data creation"

    # always clean slate test data
    # User.query.delete()

    users = [{'username': 'mary',
               'email': 'mary @ example.com',
               'password': '1234'
             }, {'username': 'john',
               'email': 'john @ example.com',
               'password': '1234'
             }]
    
    for user in users:
      u = User(username=user['username'], 
               email=user['email'], 
               password=user['password'])

      db.session.add(u)
    db.session.commit()


    pass


##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Populate the test data
    populate_users()
    