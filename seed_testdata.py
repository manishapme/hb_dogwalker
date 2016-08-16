# populate test data
# @todo use separate db for tests
from model import User, Business, Animal, Person, Service
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

    users = [{'business_id': b[0].id,
               'user_name': 'mary',
               'email': 'mary @ example.com',
               'first_name': 'Mary',
               'last_name': 'Smith',
               'password': '1234'
             }, {'business_id': b[1].id,
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


def populate_animals():
    """Create minimum sample data for the animal table."""

    print "Animals - begin data creation"

    # always clean slate test data
    Animal.query.delete()

    b = Business.query.all()

    animals = [{'business_id': b[0].id,
               'name': 'marys1Dog',
               'breed': 'pitbull',
               'birthday': '4/1/2007',
               'vet': 'Broadway Pet Hospital',
               'note': 'marys1Dog note',
               'species': 'dog'
             }, {'business_id': b[0].id,
               'name': 'marys2dog',
               'breed': 'chihuahua',
               'birthday': '9/1/2015',
               'vet': 'Broadway Pet',
               'note': 'marys2dog notes',
               'species': 'dog'
             }, {'business_id': b[0].id,
               'name': 'marys3dogsharedhousehold',
               'breed': 'husky',
               'birthday': '6/2/2013',
               'vet': 'Broadway Pet',
               'note': 'marys3dog notes',
               'species': 'dog'
             }, {'business_id': b[1].id,
               'name': 'johns1Dog',
               'breed': 'bulldog',
               'birthday': '5/5/2007',
               'vet': 'Four Seasons Animal Hospital',
               'note': 'johns1Dog note',
               'species': 'dog'
             }, {'business_id': b[1].id,
               'name': 'johns2dog',
               'breed': 'labrador',
               'birthday': '12/1/2015',
               'vet': 'Lafayette Pet',
               'note': 'johns2dog notes',
               'species': 'dog'
             }]
    
    for animal in animals:
      a = Animal(business_id=animal['business_id'],
               name=animal['name'], 
               breed=animal['breed'],
               birthday=animal['birthday'],
               vet=animal['vet'], 
               note=animal['note'],
               species=animal['species'])

      db.session.add(a)
    db.session.commit()
    return None

def populate_people():
    """Create minimum sample data for the person table."""

    print "People - begin data creation"

    # always clean slate test data
    Person.query.delete()

    b = Business.query.all()

    people = [{'business_id': b[0].id,
               'fullname': 'John Doe',
               'street': '3200 Grand Ave.',
               'city': 'Oakland',
               'state': 'CA',
               'zipcode': '94610',
               'phone': '5102222222',
               'email': 'john@doe',
               'animal': b[0].animals[0]
             }, {'business_id': b[0].id,
               'fullname': 'Jill Jones',
               'street': '1101 University Avenue',
               'city': 'Berkeley',
               'state': 'CA',
               'zipcode': '94702',
               'phone': '5105407777',
               'email': 'jill@jones',
               'animal': b[0].animals[1]
             }, {'business_id': b[1].id,
               'fullname': 'Dan Brown',
               'street': '5144 Broadway',
               'city': 'Oakland',
               'state': 'CA',
               'zipcode': '94611',
               'phone': '5106548888',
               'email': '',
               'animal': b[1].animals[0]
             }, {'business_id': b[1].id,
               'fullname': 'Amy Tan',
               'street': '1430 Fitzgerald Drive',
               'city': 'Pinole',
               'state': 'CA',
               'zipcode': '94564',
               'phone': '5107587779',
               'email': 'amy@tan',
               'animal': b[1].animals[1]
             }, ]
    

    for person in people:
        p = Person(business_id=person['business_id'],
                   fullname=person['fullname'], 
                   street=person['street'],
                   city=person['city'],
                   state=person['state'], 
                   zipcode=person['zipcode'],
                   phone=person['phone'],
                   email=person['email'])
        p.animals.append(person['animal'])
      # p.animals.append(person.animal) @todo find out why these aren't equivalent
        if person['fullname'] == 'Jill Jones': 
            p.animals.append(b[0].animals[2])   

        db.session.add(p)
    db.session.commit()
    return None


def populate_services():
    """Create minimum sample data for the services table."""

    print "Services - begin data creation"

    # always clean slate test data
    Service.query.delete()

    b = Business.query.all()

    services = [{'business_id': b[0].id, 'description': 'Walk', 'cost': 30}, 
               {'business_id': b[0].id, 'description': 'Board', 'cost': 40},
               {'business_id': b[0].id, 'description': 'Daycare', 'cost': 60}, 
               {'business_id': b[1].id, 'description': 'Walk', 'cost': 25}, 
               {'business_id': b[1].id, 'description': 'Board', 'cost': 35}, 
               {'business_id': b[1].id, 'description': 'Daycare', 'cost': 55}]
    
    for service in services:
      s = Service(business_id=service['business_id'],
               description=service['description'],
               cost=service['cost'])

      db.session.add(s)
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
    populate_animals()
    populate_people()
    populate_services()
