# all application config and route logic goes here

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (LoginManager, login_user, logout_user, login_required,
                             current_user)
from model import (User, Animal, Service, Reservation, connect_to_db, db, add_user, add_business, add_animal, 
                   add_personanimal, add_person, add_service, add_reservation) 

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] #@todo load from config file
app.jinja_env.undefined = StrictUndefined #prevent silent jinja undefined failure

#login functions provided by Flask-login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Flask-login required, get logged in user object."""

    # remember that user ids in Flask-Login are always unicode strings, 
    # so a conversion to an integer is necessary before we can send the id to Flask-SQLAlchemy.
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """The homepage."""
    if not current_user.is_authenticated:
      # @todo, session time checking. expire cookie after certain time
        return render_template('index.html')

    elif current_user.business_id:
        #a user who's signed up AND entered some business detail
        return redirect('/business/{}'.format(current_user.business.id))

    else:
        # a user who doesn't have a related business
        return redirect('/business')


@app.route('/login', methods=['POST'])
def login():
    """Process login form data and handle authentication."""

    user_name = request.form.get('user_name')
    password = request.form.get('password')
    user = User.query.filter_by(user_name=user_name, password=password).first()

    if user:
        login_user(user)
        return redirect('/business')

    else:
        flash('Error, {} and password did not match a registered user'.format(user_name))
        return redirect('/')


@app.route('/logout')
def logout():
    """Logout current user."""

    logout_user()
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """Register new user and login."""
    
    # @todo validate form data in javascript
    user_name = request.form.get('register_user_name')
    password = request.form.get('register_password')
    first_name = request.form.get('register_first_name')
    last_name = request.form.get('register_last_name')
    email = request.form.get('register_email')
    business_name = request.form.get('register_business_name')
    
    # ensure username is unique (case insensitive)
    user = User.query.filter(User.user_name.ilike(user_name)).first()

    if user:
        flash('The username {} is already in use. Please select another username.'.format(user_name))
        return redirect('/')

    else:
        new_user = add_user(user_name=user_name, password=password, 
                            first_name=first_name, last_name=last_name, email=email)
        login_user(new_user)
        # @todo needs to be broken out for future implementation of multiple users
        # @todo needs to check for duplicate businesses
        if business_name:
            # if a business name was entered, create that business and associate with this user
            new_business = add_business(business_name=business_name)
            new_user.update_user(business_id=new_business.id)
            return redirect('/business/{}'.format(new_business.id))
        else:
            return redirect('/business')


@app.route('/business')
@login_required
def show_business_page():
    """For logged in user, show detail or form to add details."""

    if current_user.business_id:
        #a user who's signed up AND entered some business detail
        return redirect('/business/{}'.format(current_user.business.id))
    else:
        #a user who's signed up, but not entered at minimum a business name
       return render_template('business.html')


@app.route('/business/<business_id>')
@login_required
def show_business(business_id):
    """For logged in user, show information about their business."""

    return render_template('business_detail.html')


@app.route('/business/update', methods=['POST'])
@login_required
def update_business_():
    """Allow user to update business info."""

    # suffix of '_' on functionname to avoid name collision with method

    r = request.form
    b = current_user.business
    b.update_business(
                      business_name=r.get('business_name'),
                      business_street=r.get('street'),
                      business_city=r.get('city'),
                      business_state=r.get('state'),
                      business_zip=r.get('zip'),
                      business_phone=r.get('phone'),
                      url=r.get('url'),
                      license=r.get('license')
                      )
    return jsonify(result=b.business_name)


@app.route('/business/add', methods=['POST'])
@login_required
def add_business_():
    """Allow user to add business if not already defined."""

    # suffix of '_' on functionname to avoid name collision with method

    r = request.form
    new_business = add_business(
                                business_name=r.get('business_name'),
                                business_street=r.get('street'),
                                business_city=r.get('city'),
                                business_state=r.get('state'),
                                business_zip=r.get('zip'),
                                business_phone=r.get('phone'),
                                url=r.get('url'),
                                license=r.get('license')
                               )


    #after creating new business, ensure it is associated with current user
    #@todo, if we ever have a superadmin role, this breaks
    current_user.update_user(business_id=new_business.id)

    return redirect('/business/{}'.format(current_user.business.id))


@app.route('/animal/add', methods=['POST'])
@login_required
def add_animal_():
    """Add animals to a specific business."""

    r = request.form
    a = add_animal(
                   business_id=r.get('business_id', current_user.business.id), 
                   name=r.get('name'),
                   species=r.get('species'), 
                   breed=r.get('breed'), 
                   # because a datetime field cannot accept an empty string, must set value to None
                   birthday=r.get('birthday') or None, 
                   vet=r.get('vet'),
                   note=r.get('note'),
                 )
    # if they've included person data we also create a person
    if r.get('fullname'):
        p = add_person(
                       # these fields for adding a person. might not be added at same time @todo??
                       business_id=r.get('business_id', current_user.business.id), 
                       fullname=r.get('fullname'),
                       street=r.get('street'),
                       city=r.get('city'),
                       state=r.get('state'),
                       zipcode=r.get('zipcode'),
                       phone=r.get('phone'),
                       email=r.get('email')
                      )
        # if they added a person we also add the join record at same time
        add_personanimal(a, p)

    return redirect('/business/{}'.format(current_user.business.id))


@app.route('/animal/<animal_id>')
@login_required
def show_animal(animal_id):
    """List details for selected animal and relations."""

    a = Animal.query.get(int(animal_id))
    other_animals = []
    for p in a.people:
        for other in p.animals:
            other_animals.append(other)

    # @todo ask about syntax of joined load a = db.session.query.filter(Animal.id == int(animal_id)).options(db.joinedload('person')).all()
    return render_template('animal.html', animal=a, other_animals=other_animals)


@app.route('/service/add', methods=['POST'])
@login_required
def add_service_():
    """Add a service for current business."""

    r = request.form
    s = add_service(business_id=r.get('business_id', current_user.business.id), 
                    description=r.get('description'),
                    cost=r.get('cost'))

    return redirect('/business/{}'.format(current_user.business.id))

@app.route('/reservation')
@login_required
def show_reservations():
    """Show all reservations for a specific business."""

    # join using the relationship attribute.                 gives you access to other table
    res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                 == current_user.business.id).all()
    ser = current_user.business.services

    return render_template('reservation.html', reservations=res, services=ser)

@app.route('/reservation/add', methods=['POST'])
@login_required
def add_reservation_():
    """Add a reservation for a specific business."""

    r = request.form
    a = Animal.query.get(r.get('animal_id'))
    person_id = a.people[0].id
    print person_id

    res = add_reservation(
                 animal_id=r.get('animal_id'), 
                 person_id=r.get('person_id') or person_id, 
                 service_id=r.get('service_id'),
                 event_id=r.get('event_id') or None,
                 invoice_id=r.get('invoice_id') or None,
                 start_date=r.get('start_date'),
                 end_date=r.get('end_date'),
                 cost=r.get('cost'),
                 note=r.get('note')
                 )

    return redirect('/reservation')

@app.route('/schedule')
@login_required
def show_schedule():
    """Allow user to view reservations on a map."""

    # begin with all reservations
    res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                 == current_user.business.id).all()
    #then grab the animal each reservation pertains to
    animals_list = []
    for r in res:
        animals_list.append(r.animal)

    #then grab the person/address for each animal
    # @todo modify relationships so this works if there is more than one person
    # @todo, grab person id when making the reservation
    # print animals

    # return render_template('schedule.html', people=people)
    return render_template('schedule.html', animals=animals_list)


# @app.route('/schedule/<start_date>/<end_date>')


if __name__ == '__main__':

    app.debug = True # app.debug = os.environ['FLASK_DEBUG']
   # only show toolbar when debug is true
    if app.debug:
        DebugToolbarExtension(app) 


    connect_to_db(app)

    # we are setting the host to 0.0.0.0 because we are running in vagrant
    # if using Mac's python would not need to be specified
    app.run(host='0.0.0.0')
