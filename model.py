"""Models and database functions for dogwalker application."""

from flask_sqlalchemy import SQLAlchemy


# create instance of SQLAlchemy from which we will call all db functions
db = SQLAlchemy()


##############################################################################
# Models

class User(db.Model):
    """Individual User of application."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def is_active(self):
        """True, as all users are active in the current implementation."""
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
           authenticate for some reason.

           http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        """
        return True


    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Business(db.Model):
    """A business tied to a specific User of application."""

    __tablename__ = "business"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    business_name = db.Column(db.String(108), nullable=False)


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


##############################################################################

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dogwalker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.app = app
    db.init_app(app)