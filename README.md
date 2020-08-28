# Star Tours
A mock travel site for Star Wars planets.  Using data taken from the Star Wars API, or [SWAPI](https://swapi.dev/).

## Proposal

### Goal
The goal I will try to achieve with my Star Tours website is to allow users to book trips and speciality tours to planets within the Star Wars universe, with help from the Star Wars API.  

### User Demographic
I believe the ***main*** demographic of my website will be adults anywhere from 25 - 60 years old.  Obviously, Star Wars fans and sci-fi fans in general will be a huge demographic as well.  Also, in the realm of my make-believe world where this website is real, my website will be tailored to users from Earth, using Earth data to compare conditions here to conditions on other planets.

### Data
Using the Star Wars API, I plan to use the API's data to get each planet's:

1. name
2. rotation period (how long the days are)
3. orbital period (how long the years are)
4. diameter
5. climate
6. gravity (compared to Earth)
7. terrain
8. surface water amount
9. population
10. famous residents

In addition to this data, I also definitely want to add to each planet:

1. A/a few picture(s) of the planet
2. A/a few tour(s) associated with the planet
3. A short description of the planet and what there is to do

### Approach
My database schema is going to look like this...

`class User(db.Model):`

    __tablename__ = 'users'

    email = db.Column(db.Text, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    trips = db.relationship('Trip', backref='user', cascade='all, delete-orphan')


`class Flight(db.Model):`

    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_num = db.Column(db.Integer, nullable=False)
    depart_datetime = db.Column(db.DateTime, nullable=False)
    arrive_datetime = db.Column(db.DateTime, nullable=False)
    depart_planet = db.Column(db.Text, nullable=False)
    arrive_planet = db.Column(db.Text, nullable=False)
    depart_port = db.Column(db.Text, nullable=False)
    arrive_port = db.Column(db.Text, nullable=False)

`class Trip(db.Model):`

    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text, db.ForeignKey('users.email'))

    flights = db.relationship('Flight', secondary='trips_flights', backref='trips')
    planets = db.relationship('Planet', secondary='trips_planets', backref='trips')
    tours = db.relationship('Tour', secondary='trips_tours', backref='trips')

`class TripFlight(db.Model):`

    __tablename__ = 'trips_flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))

`class TripPlanet(db.Model):`

    __tablename__ = 'trips_planets'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    planet = db.Column(db.Integer, db.ForeignKey('planets.name'))

`class TripTour(db.Model):`

    __tablename__ = 'trips_tours'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))

`class Planet(db.Model):`

    __tablename__ = 'planets'

    name = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    tours = db.relationship('Tour', backref='planet', cascade='all, delete-orphan')

`class Tour(db.Model):`

    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    planet = db.Column(db.Text, db.ForeignKey('planets.name'))

The main issue I may encounter with the Star Wars API is that I really want to tweak some of the data so it makes more sense and that it's also missing some important data, mainly a picture.  I don't know if I'm just going to have to manually enter this extra data myself for each planet, or if there's an easier, faster, and dynamic way of doing this.

There will definitely be user passwords that I'll need to encrypt.  I'm still not sure of how booking will work.  We haven't covered taking people's payment information yet, so I wouldn't even know how to do that, and more importantly, I don't want anyone spending any of their money on my site.  So, don't know how I'm going to fake this part yet, but maybe just a simple form that will take imaginary money.  Maybe they'll enter a fake credit card number?  Or maybe I'll just make everything free.

I want my site to allow users to create an account, book trips to planets, and if they want, tours associated with that planet, view their trips (itineraries) in their account, allow them to cancel their trip or tour, allow them to edit their trip or tour, allow them to add another planet and/or tour to their trip, and delete their profile.  
