"""Models and database functions for dogwalker application."""

from flask_sqlalchemy import SQLAlchemy


# create instance of SQLAlchemy from which we will call all db functions
db = SQLAlchemy()


##############################################################################
# Models

class User(db.Model):
    """Individual User of application."""

    __tablename__ = 'users' # NOTE 'user' is reserved table in postgres. can't use as tablename

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    user_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    business = db.relationship('Business', backref=db.backref('users', order_by=first_name))


    def is_active(self):
        """True, as all users are active in the current implementation. 

        Flask-Login requirement."""
        return True


    def get_id(self):
        """Return the id as unicode to satisfy Flask-Login's requirements."""
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3


    def is_authenticated(self):
        """In general this method should just return True.

           Unless the object represents a user that should not be allowed to 
           authenticate for some reason. Flask-Login requirement.

           http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        """
        return True


    def is_anonymous(self):
        """False, as anonymous users aren't supported.

           Flask-Login requirement.
        """
        return False

    def update_user(self, **kwargs):
        """Update existing user data."""

        self.user_name = kwargs.get('user_name', self.user_name)
        self.password = kwargs.get('password', self.password)
        self.first_name = kwargs.get('first_name', self.first_name)
        self.last_name = kwargs.get('last_name', self.last_name)
        self.email = kwargs.get('email', self.email)
        self.business_id = kwargs.get('business_id', self.business_id)

        db.session.commit()
        return self





class Business(db.Model):
    """A business tied to a specific User of application."""

    __tablename__ = 'business'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_name = db.Column(db.String(108), nullable=False)
    business_street = db.Column(db.String(108))
    business_city = db.Column(db.String(64))
    business_state = db.Column(db.String(2))
    business_zip = db.Column(db.String(9))
    business_phone = db.Column(db.String(10))
    url = db.Column(db.String(64))
    license = db.Column(db.String(64))


    def update_business(self, **kwargs):
        """Update data for this one business."""

        self.business_name = kwargs.get('business_name', self.business_name)
        self.business_street = kwargs.get('business_street', self.business_street)
        self.business_city = kwargs.get('business_city', self.business_city)
        self.business_state = kwargs.get('business_state', self.business_state)
        self.business_zip = kwargs.get('business_zip', self.business_zip)
        self.business_phone = kwargs.get('business_phone', self.business_phone)
        self.url = kwargs.get('url', self.url)
        self.license = kwargs.get('license', self.license)

        db.session.commit()
        return self

# A many-to-many association requiring only keys DOESN'T require a class definition  
# note must appear before the classes it joins
personanimal = db.Table('personanimal', 
    db.Column('person_id', db.Integer, db.ForeignKey('person.id')),
    db.Column('animal_id', db.Integer, db.ForeignKey('animal.id'))
    )


class Animal(db.Model):
    """An animal that is serviced by a business."""

    __tablename__ = 'animal'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    name = db.Column(db.String(64), nullable=False)
    breed = db.Column(db.String(64), nullable=True)
    birthday = db.Column(db.DateTime)
    vet = db.Column(db.Text)
    note = db.Column(db.Text)
    species = db.Column(db.String(64))

    business = db.relationship('Business', backref=db.backref('animals', order_by=name))
    people = db.relationship('Person', secondary=personanimal, backref=db.backref('personanimal'))


class Person(db.Model):
    """A person that is responsible for one or more animals."""

    __tablename__ = 'person'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    fullname = db.Column(db.String(164), nullable=False)
    street = db.Column(db.String(108))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(9))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(64))

    business = db.relationship('Business', backref=db.backref('people', order_by=fullname))
    animals = db.relationship('Animal', secondary=personanimal, backref=db.backref('personanimal'))


class Service(db.Model):
    """A service that a business provides."""


    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))
    description = db.Column(db.String(164), nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    business = db.relationship('Business', backref=db.backref('services', order_by=description))



##############################################################################
# CREATE, DELETE functions
def add_user(user_name, password, first_name, last_name, email):
    """Add new user."""

    user = User(user_name=user_name,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email)

    db.session.add(user)
    db.session.commit()
    return user


def add_business(**kwargs):
    """Add new business."""

    b = Business(business_name=kwargs.get('business_name'), 
                 business_street=kwargs.get('business_street'),
                 business_city=kwargs.get('business_city'), 
                 business_state=kwargs.get('business_state'), 
                 business_zip=kwargs.get('business_zip'), 
                 business_phone=kwargs.get('business_phone'), 
                 url=kwargs.get('url'), 
                 license=kwargs.get('license')
                 )

    db.session.add(b)
    db.session.commit()
    return b


def add_animal(**kwargs):
    """Add new animal."""

    a = Animal(
                 business_id=kwargs.get('business_id'), 
                 name=kwargs.get('name'),
                 species=kwargs.get('species'), 
                 breed=kwargs.get('breed'), 
                 birthday=kwargs.setdefault('birthday', None), 
                 vet=kwargs.get('vet'),
                 note=kwargs.get('note')
                 )

    db.session.add(a)
    db.session.commit()
    return a


def add_person(**kwargs):
    """Add new person."""

    p = Person(
                 business_id=kwargs.get('business_id'), 
                 fullname=kwargs.get('fullname'),
                 street=kwargs.get('street'), 
                 city=kwargs.get('city'), 
                 state=kwargs.get('state'), 
                 zipcode=kwargs.get('zipcode'),
                 phone=kwargs.get('phone'),
                 email=kwargs.get('email')
                 )

    db.session.add(p)
    db.session.commit()
    return p

def add_personanimal(animal_obj, person_obj):
    """Create an association between a person and animal."""

    animal_obj.people.append(person_obj)
    db.session.commit()


def add_service(**kwargs):
    """Add new animal."""

    s = Service(
                 business_id=kwargs.get('business_id'), 
                 description=kwargs.get('description'),
                 cost=kwargs.get('cost')
                 )

    db.session.add(s)
    db.session.commit()
    return s

##############################################################################

def connect_to_db(app, db_uri='postgresql:///dogwalker'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.app = app
    db.init_app(app)