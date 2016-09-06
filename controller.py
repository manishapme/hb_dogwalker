# all application config and route logic goes here

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
import requests
import json
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import (LoginManager, login_user, logout_user, login_required,
                             current_user)
from model import (User, Person, Animal, Service, Business, Reservation, connect_to_db, db, add_user, add_business, add_animal, 
                   add_personanimal, add_person, add_service, add_reservation, get_animals_list) 
from sqlalchemy.sql import func
import dictalchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] #@todo load from config file
app.jinja_env.undefined = StrictUndefined #prevent silent jinja undefined failure
bcrypt = Bcrypt(app)

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
        return redirect('/business/{}'.format(current_user.business_id))

    else:
        # a user who doesn't have a related business
        return redirect('/business')


@app.route('/login', methods=['POST'])
def login():
    """Process login form data and handle authentication."""

    user_name = request.form.get('user_name')
    password = request.form.get('password')
    user = User.query.filter_by(user_name=user_name).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect('/')

    else:
        flash('Error, {} and password did not match a registered user'.format(user_name))
        return redirect('/')


@app.route('/logout')
def logout():
    """Logout current user."""

    logout_user()
    if session.get('start_date'):
        del session['start_date']

    if session.get('res_count'):
        del session['res_count']
    
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
    # store password as hash
    password = bcrypt.generate_password_hash(password)
    
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
            new_business = add_business(business_name=business_name,
                                business_street='',
                                business_city='',
                                business_state='',
                                business_zip='',
                                business_phone='',
                                url='',
                                license='')
            new_user.update_user(business_id=new_business.id)
            return redirect('/business/{}'.format(current_user.business_id))
        else:
            return redirect('/business')


@app.route('/business/<business_id>')
@app.route('/business')
@login_required
def show_business_page(business_id=None):
    """For logged in user, show detail or form to add details."""

    if current_user.business_id:
        #a user who's signed up AND entered some business detail
        return render_template('business_detail.html')
    else:
        #a user who's signed up, but not entered at minimum a business name
       return render_template('business.html')


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

    return jsonify(dictalchemy.utils.asdict(b))


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

    return redirect('/business/{}'.format(current_user.business_id))



@app.route('/animal')
@login_required
def show_animal_all():
    """List all animals for this business."""

    return render_template('animal.html')


@app.route('/animal/add', methods=['POST'])
@login_required
def add_animal_():
    """Add animals to a specific business."""

    r = request.form
    a = add_animal(
                   business_id=r.get('business_id', current_user.business_id), 
                   name=r.get('name'),
                   species=r.get('species'), 
                   breed=r.get('breed'), 
                   # because a datetime field cannot accept an empty string, must set value to None
                   birthday=r.get('birthday') or None, 
                   vet=r.get('vet'),
                   note=r.get('note'),
                   photo_path=r.get('photo_path')
                 )
    # if they've included person data we also create a person
    if r.get('fullname'):
        p = add_person(
                       # these fields for adding a person. might not be added at same time @todo??
                       business_id=r.get('business_id', current_user.business_id), 
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

    animals = get_animals_list(current_user.business_id, 'json')
    return jsonify(animals)


@app.route('/animal/<animal_id>')
@login_required
def show_animal(animal_id):
    """List details for selected animal and relations."""

    a = Animal.query.get(animal_id)
    other_animals = []
    for p in a.people:
        for other in p.animals:
            if other.id != a.id:
                other_animals.append(other)

    # @todo ask about syntax of joined load a = db.session.query.filter(Animal.id == int(animal_id)).options(db.joinedload('person')).all()
    return render_template('animal_detail.html', animal=a, other_animals=other_animals)


@app.route('/animal/<animal_id>/update', methods=['POST'])
@login_required
def update_animal_(animal_id):
    """Add a service for current business."""

    r = request.form
    a = Animal.query.get(animal_id)
    a.update_animal(
                   name=r.get('name'),
                   species=r.get('species'), 
                   breed=r.get('breed'), 
                   # because a datetime field cannot accept an empty string, must set value to None
                   birthday=r.get('birthday') or None, 
                   vet=r.get('vet'),
                   note=r.get('note'),
                   photo_path=r.get('photo_path')
                 )

    if r.get('fullname'):
        p = Person.query.get(a.people[0].id)
        p.update_person(
                       # these fields for adding a person. might not be added at same time @todo??
                       fullname=r.get('fullname'),
                       street=r.get('street'),
                       city=r.get('city'),
                       state=r.get('state'),
                       zipcode=r.get('zipcode'),
                       phone=r.get('phone'),
                       email=r.get('email')
                      )
    return redirect('/animal/{}'.format(animal_id))


@app.route('/animal/<animal_id>/add/person', methods=['POST'])
@login_required
def add_person_(animal_id):
    """Add person to existing animal."""

    r = request.form

    a = Animal.query.get(animal_id)
    p = add_person(
                   # these fields for adding a person. might not be added at same time @todo??
                   business_id=r.get('business_id', current_user.business_id), 
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

    return redirect('/animal/{}'.format(animal_id))


@app.route('/service/add', methods=['POST'])
@login_required
def add_service_():
    """Add a service for current business."""

    r = request.form
    s = add_service(business_id=r.get('business_id', current_user.business_id), 
                    description=r.get('description'),
                    cost=r.get('cost'))

    return redirect('/business/{}'.format(current_user.business_id))



@app.route('/service/update', methods=['POST'])
@login_required
def update_service_():
    """Add a service for current business."""

    r = request.form
    s = Service.query.get(r.get('id'))
    s.update_service(description=r.get('description'),
                    cost=r.get('cost'))

    return redirect('/business/{}'.format(current_user.business_id))


@app.route('/reservation')
@login_required
def show_reservations():
    """Show all reservations for a specific business."""

    # join using the relationship attribute.                 gives you access to other table
    # filter reservations if date chosen
    if session.get('start_date'): 
        res_date = session['start_date']
        res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                             == current_user.business_id, 
                                             func.date(Reservation.start_date) == res_date).all()
    else:
        res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                     == current_user.business_id).all()

    ser = current_user.business.services

    if res:
        session['res_count'] = True

    return render_template('reservation.html', reservations=res, services=ser)


@app.route('/reservation/date/<format_json>')
@app.route('/reservation/date')
@login_required
def filter_reservations(format_json=None):
    """Show the reservations for a specficied date"""

    res_date = request.args.get('date_filter')
    biz_id = current_user.business_id
    # stash res_date so it can be prepopulated 
    session['start_date'] = res_date
    
    res = Reservation.query.join(Reservation.service).filter(Service.business_id == biz_id, func.date(Reservation.start_date) == res_date).all()
    ser = current_user.business.services

    if not format_json:
        return render_template('reservation.html', reservations=res, services=ser)
    else:
        # coming from the map page and asking for addresses as json
        res_dict = []
        for r in res:
            # need the animal/address info more than the reservation
            r_dict = {}
            r_dict['address'] = r.animal.people[0].format_address()
            r_dict['animal_id'] = r.animal_id
            r_dict['animal_name'] = r.animal.name
            res_dict.append(r_dict)

        return jsonify(res_dict) 


@app.route('/reservation/timeline/<format_json>')
@app.route('/reservation/timeline')
@login_required
def show_reservations_on_timeline(format_json=None):
    """Return all reservations as json for display on timeline"""

    biz_id = current_user.business_id
    
    res = Reservation.query.join(Reservation.service).filter(Service.business_id == biz_id).all()
    res_dict = []
    for r in res:
        # need the animal/address info more than the reservation
        r_dict = {}
        r_dict['id'] = r.id
        r_dict['content'] = r.animal.name
        r_dict['title'] = r.service.description
        r_dict['start'] = '{:%Y-%m-%d}'.format(r.start_date)
        if r_dict['start'] != '{:%Y-%m-%d}'.format(r.end_date):
            r_dict['type'] = 'range'
            r_dict['end'] = '{:%Y-%m-%d}'.format(r.end_date)
            r_dict['group'] = 1
        else:
            r_dict['type'] = 'point'
            r_dict['group'] = 0
        res_dict.append(r_dict)

    if not format_json:
        return render_template('timeline.html')
    else:
        return jsonify(res_dict) 


@app.route('/reservation/add', methods=['POST'])
@login_required
def add_reservation_():
    """Add a reservation for a specific business."""

    r = request.form
    a = Animal.query.get(r.get('animal_id'))
    person_id = a.people[0].id

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

    session['res_count'] = True
    return redirect('/reservation')


@app.route('/reservation/map')
@login_required
def show_map():
    """Allow user to view reservations on a map."""

    # filter reservations if date chosen
    if session.get('start_date'): 
        res_date = session['start_date']
        res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                             == current_user.business_id, 
                                             func.date(Reservation.start_date) == res_date).all()
    else:
        res = Reservation.query.join(Reservation.service).filter(Service.business_id
                                     == current_user.business_id).all()

    #then grab the animal each reservation pertains to
    animals_list = []
    for r in res:
        animals_list.append(r.animal)

    return render_template('map.html', animals=animals_list)


@app.route('/geocode')
def geocode_address():
    """Take a given address and geocode it."""

    address = current_user.business.format_address().replace(' ', '%20')
    print address
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+os.environ['GOOGLE_MAPS_KEY']
    print url
    r = requests.get(url).content
    r = json.loads(r)
    r = r.get('results')
    r = r[0].get('geometry')
    r = r.get('location')

    return "hello"


@app.template_filter('strftime')
def date_format(value, format='%B %d, %Y'):
    """Custom filter for formatting datetime object as date in Jinja."""

    return value.strftime(format)
# jinja_env.filters['datetime'] = format_datetime


if __name__ == '__main__':

    app.debug = True # app.debug = os.environ['FLASK_DEBUG']
   # only show toolbar when debug is true
    # if app.debug:
    #     DebugToolbarExtension(app) 


    connect_to_db(app)

    # we are setting the host to 0.0.0.0 because we are running in vagrant
    # if using Mac's python would not need to be specified
    app.run(host='0.0.0.0')
