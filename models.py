from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.Text, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    trips = db.relationship('Trip', backref='user', cascade='all, delete-orphan')


class Flight(db.Model):
    # How would I continually update my flights on this project?  Would I just have to keep updating and running a seed file every now and then?
    # Or is there some way to automate this?  Or should I just get rid of this model completely?

    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_num = db.Column(db.Integer, nullable=False)
    depart_datetime = db.Column(db.DateTime, nullable=False)
    arrive_datetime = db.Column(db.DateTime, nullable=False)
    depart_planet = db.Column(db.Text, nullable=False)
    arrive_planet = db.Column(db.Text, nullable=False)
    depart_port = db.Column(db.Text, nullable=False)
    arrive_port = db.Column(db.Text, nullable=False)

class Trip(db.Model):
    # I was debating on adding this model.  I'm pretty sure I can set it up where I can get all of this info directly from
    # inside my User model, but this seemed cleaner and more organized.
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Text, db.ForeignKey('users.email'))

    # Should I add any ON DELETE CASCADEs to any of these relationships?  I feel like if I delete any planets, flights, or tours
    # this model won't be affected by that, because these aren't technically columns of data, they're just relationships
    flights = db.relationship('Flight', secondary='trips_flights', backref='trips')
    planets = db.relationship('Planet', secondary='trips_planets', backref='trips')
    tours = db.relationship('Tour', secondary='trips_tours', backref='trips')

# Could I do without these 3 classes below and just have done a class TripFlightPlanetTour?

class TripFlight(db.Model):
    # Do these middle tables get updated when I append info from another relationship?
    # For instance, if I just appended flight info in a Trip object, would this table be automatically updated with the correct data?
    __tablename__ = 'trips_flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # would it be easier/make more sense to just make these things below my primary_key (both of them together)?  
    # or should I just stick to having the primary_key be a separate number id?
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))

class TripPlanet(db.Model):
    __tablename__ = 'trips_planets'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    planet = db.Column(db.Integer, db.ForeignKey('planets.name'))

class TripTour(db.Model):
    __tablename__ = 'trips_tours'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))

class Planet(db.Model):
    __tablename__ = 'planets'

    name = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=False)

    tours = db.relationship('Tour', backref='planet', cascade='all, delete-orphan')

class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    planet = db.Column(db.Text, db.ForeignKey('planets.name'))