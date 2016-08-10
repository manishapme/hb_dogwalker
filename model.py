"""Models and database functions for dogwalker application."""

from flask_sqlalchemy import SQLAlchemy


# create instance of SQLAlchemy from which we will call all db functions
db = SQLAlchemy()


##############################################################################
# Models

class User(db.Model):
    """Individual User of application."""

    __tablename__ = 'users' # NOTE 'user' is reserved table in psql. can't use as tablename

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'))
    user_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    business = db.relationship('Business', backref=db.backref('users', order_by=first_name))

    # business = db.relationship('Business', backref=db.backref('users', order_by(first_name, last_name)))

    def is_active(self):
        """True, as all users are active in the current implementation. 

        Flask-Login requirement."""
        return True


    def get_id(self):
        """Return the id as unicode to satisfy Flask-Login's requirements."""
        try:
            return unicode(self.user_id)  # python 2
        except NameError:
            return str(self.user_id)  # python 3


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


class Business(db.Model):
    """A business tied to a specific User of application."""

    __tablename__ = 'business'

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_name = db.Column(db.String(108), nullable=False)
    business_street = db.Column(db.String(108))
    business_city = db.Column(db.String(64))
    business_state = db.Column(db.String(2))
    business_zip = db.Column(db.String(9))
    business_phone = db.Column(db.String(10))
    url = db.Column(db.String(64))
    license = db.Column(db.String(64))



##############################################################################
# CREATE, UPDATE, DELETE functions
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


# def update_user(user_id, business_name):
#     """Update existing user data."""

#     user = User(user_name=user_name,
#                 password=password,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email)

#     db.session.add(user)
#     db.session.commit()
#     return user


def add_business(business_name, business_street='', business_city='',
                 business_state='', business_zip='', business_phone='', url='',
                 license=''):

    """Add new business."""

    b = Business(business_name=business_name, business_street=business_street,
                 business_city=business_city, business_state=business_state, 
                 business_zip=business_zip, business_phone=business_phone, 
                 url=url, license=license)

    db.session.add(b)
    db.session.commit()
    return b

##############################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dogwalker'

    db.app = app
    db.init_app(app)