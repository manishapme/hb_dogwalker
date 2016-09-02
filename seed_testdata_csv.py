# populate test data
# @todo use separate db for tests
from model import User, Business, Animal, Person, Service, Reservation
from model import connect_to_db, db
from controller import app, bcrypt

def populate_business():
    """Create minimum sample data for the business table."""


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

    # always clean slate test data
    User.query.delete()

    b = Business.query.all()
    p1 = bcrypt.generate_password_hash('1234')
    p2 = bcrypt.generate_password_hash('1234')

    users = [{'business_id': b[0].id,
               'user_name': 'mary',
               'email': 'mary @ example.com',
               'first_name': 'Mary',
               'last_name': 'Smith',
               'password': p1
             }, {'business_id': b[1].id,
               'user_name': 'john',
               'email': 'john @ example.com',
               'first_name': 'John',
               'last_name': 'Baker',
               'password': p2
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

    Animal.query.delete()

    for i, row in enumerate(open('seed_data/dogs.csv')):
        business_id, name, species, breed, birthday, vet, note, photo_path = row.rstrip().split(",")

        a = Animal(business_id=business_id,
               name=name, 
               breed=breed,
               birthday=birthday,
               vet=vet, 
               note=note,
               species=species,
               photo_path=photo_path)
        db.session.add(a)
    db.session.commit()
    return None


def populate_people():
    """Create minimum sample data for the person table."""

    # always clean slate test data
    Person.query.delete()
    animals = Animal.query.all()

    for i, row in enumerate(open('seed_data/people.csv')):
        business_id, fullname, street, city, state, zipcode, phone, email = row.rstrip().split(',')

        p = Person(business_id=business_id,
                   fullname=fullname, 
                   street=street,
                   city=city,
                   state=state, 
                   zipcode=zipcode,
                   phone=phone,
                   email=email)
        a = animals[i]
        p.animals.append(a)
        db.session.add(p)
    db.session.commit()
    return None


def populate_services():
    """Create minimum sample data for the services table."""

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


def populate_reservations():
    """Create minimum sample data for the reservations table."""

    Reservation.query.delete()
    
    for i, row in enumerate(open('seed_data/reservations.csv')):
        animal_id, person_id, service_id, start_date, end_date, cost, note = row.rstrip().split(',')

        r = Reservation(
                        animal_id=animal_id,
                        person_id=person_id,
                        service_id=service_id,
                        start_date=start_date,
                        end_date=end_date,
                        cost=cost,
                        note=note
            )
        db.session.add(r)
    db.session.commit()
    return None



##############################################################################
if __name__ == "__main__":
    connect_to_db(app)

    # For housekeeping, clean slate
    db.drop_all()
    db.create_all()

    # Populate the test data
    print "Business - begin data creation"
    populate_business()
    print "User - begin data creation"    
    populate_users()
    print "Animals - begin data creation"
    populate_animals()    
    print "People - begin data creation"
    populate_people()
    print "Services - begin data creation"
    populate_services()
    print 'Reservations - begin data creation.'
    populate_reservations()
