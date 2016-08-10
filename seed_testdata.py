# populate test data
# @todo use separate db for tests
from model import User, Business
from model import connect_to_db, db
from controller import app

def populate_business():
    """Create minimum sample data for the business table."""

    print "Business - begin data creation"

    # always clean slate test data
    Business.query.delete()

    businesses = [{'business_name': 'Lobodogwalks',
                   'business_street': '43621 Pacific Commons Blvd.',
                   'business_city': 'Fremont',
                   'business_state': 'CA',
                   'business_zip': '94538',
                   'business_phone': '510111111',
                   'url': 'http://Lobodogwalks.com',
                   'license': 'def567'}, 
                  {'business_name': 'Ruff Tails',
                   'business_street': '4801 Central Ave.',
                   'business_city': 'Richmond',
                   'business_state': 'CA',
                   'business_zip': '94804',
                   'business_phone': '5102222222',
                   'url': 'http://rufftails.com',
                   'license': 'abc123'}]

    for business in businesses:
      b = Business(business_name=business['business_name'], 
               business_street=business['business_street'],
               business_city=business['business_city'],
               business_state=business['business_state'], 
               business_zip=business['business_zip'], 
               business_phone=business['business_phone'], 
               url=business['url'], 
               license=business['license'])

      db.session.add(b)
    db.session.commit()
    return None


def populate_users():
    """Create minimum sample data for the user table."""

    print "User - begin data creation"

    # always clean slate test data
    User.query.delete()

    b = Business.query.all()

    users = [{'business_id': b[0].business_id,
               'user_name': 'mary',
               'email': 'mary @ example.com',
               'first_name': 'Mary',
               'last_name': 'Smith',
               'password': '1234'
             }, {'business_id': b[1].business_id,
               'user_name': 'john',
               'email': 'john @ example.com',
               'first_name': 'John',
               'last_name': 'Baker',
               'password': '1234'
             }]
    
    for user in users:
      u = User(business_id=user['business_id'],
               user_name=user['user_name'], 
               first_name=user['first_name'],
               last_name=user['last_name'],
               email=user['email'], 
               password=user['password'])

      db.session.add(u)
    db.session.commit()
    return None



##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    # For housekeeping, clean slate
    db.drop_all()
    db.create_all()

    # Populate the test data
    populate_business()
    populate_users()
    