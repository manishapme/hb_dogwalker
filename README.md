![Dogwalker Logo](/static/images/logo.png)

Dogwalker is a small business manager targeting the pet care professional. Most individuals working with pets have talents and skills in relating to animals. Many are also sole proprietors who must also manage administrative tasks.

This tool is a multi-user web application for these individuals to make the office management part of their business simpler. It gives them a place to track information about the pets they care for, the humans that pay the bills, create reservations and view their upcoming schedule. 

It is deployed at: <a src="http://hb-dogwalker.herokuapp.com/">http://hb-dogwalker.herokuapp.com/</a>
 

## Table of Contents
* [Technologies Used](#technologiesused)
* [ERD](#ERD)
* [How it works](#how)
* [Version 1.0](#v1)
* [Author](#author)

## <a name="technologiesused"></a>Technologies Used
* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask - SQLAlchemy](http://flask.pocoo.org/)
* [Flask - Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask - Bcrypt](http://flask-bcrypt.readthedocs.io/en/latest/)
* [PostgreSQL](https://www.postgresql.org)
* [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
* [jQuery](https://jquery.com/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [Bootstrap](http://getbootstrap.com)
* [Google Maps Directions API](https://developers.google.com/maps/documentation/javascript/directions)
* [Vis.js Timeline](http://visjs.org)

## <a name="ERD"></a>ERD
Version one launched with a normalized data model built for a limited set of features. The User, Business, Service, Person, Animal, Reservation and PersonAnimal entities were created and represent a variety of joins. The model allows easy extension of the additional entities required to support the next set of features.

![PDF](/static/images/readme/erd_dogwalker.png)

## <a name="how"></a>How it works
####Registration
As a multi-user solution, the system requires registration and authentication. Passwords are hashed and stored in encrypted form.

![Registration](/static/images/readme/homepage.png)

####Business Overview
After the user is registered, they are able to view the details of their business on the overview page. This page is initially rendered by Jinja, but adding and editing is handled via ajax requests.

![Overview](/static/images/readme/overview.png)

####Routing
Users can view the reservations for a specified day and map a route via the Google Directions API. The addressess for all scheduled pets are are collected from the page using jQuery and passed to the API as a list of waypoints. The opitimize parameter (for Google Directions API) is set to ensure user receives the most efficient directions. 

![Routing](/static/images/readme/map.png)

####Timeline
Users can view the reservations on a timeline using the vis.js library. 

![Timeline](/static/images/readme/timeline.png)

## <a name="v1"></a>Version 1.0

Future phases will enable invoicing, uploading photos and automate messaging of photos to owners. This allows business to communicate to pet-owners while building an organized history of their activities. The system will also be mobile optimized.

## <a name="author"></a>Author
Manisha Patel is a software engineer from the San Francisco Bay area.