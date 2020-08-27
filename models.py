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

    itinerariess = db.relationship('Itinerary', backref='user', cascade='all, delete-orphan')


class Flight(db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_num = db.Column(db.Integer, nullable=False)
    depart_planet = db.Column(db.Text, nullable=False)
    arrive_planet = db.Column(db.Text, nullable=False)
    depart_port = db.Column(db.Text, nullable=False)
    arrive_port = db.Column(db.Text, nullable=False)

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    depart_datetime = db.Column(db.DateTime, nullable=False)
    arrive_datetime = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.Text, db.ForeignKey('users.email'))

    # Should I add any ON DELETE CASCADEs to any of these relationships?  I feel like if I delete any planets, flights, or tours
    # this model won't be affected by that, because these aren't technically columns of data, they're just relationships
    flights = db.relationship('Flight', secondary='itineraries_flights', backref='itineraries')
    planets = db.relationship('Planet', secondary='itineraries_planets', backref='itineraries')
    tours = db.relationship('Tour', secondary='itineraries_tours', backref='itineraries')

# Could I do without these 3 classes below and just have done a class ItineraryFlightPlanetTour?

class ItineraryFlight(db.Model):
    # Do these middle tables get updated when I append info from another relationship?
    # For instance, if I just appended flight info in a Itinerary object, would this table be automatically updated with the correct data?
    __tablename__ = 'itineraries_flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # would it be easier/make more sense to just make these things below my primary_key (both of them together)?  
    # or should I just stick to having the primary_key be a separate number id?
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'))

class ItineraryPlanet(db.Model):
    __tablename__ = 'itineraries_planets'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))
    planet = db.Column(db.Integer, db.ForeignKey('planets.name'))

class ItineraryTour(db.Model):
    __tablename__ = 'itineraries_tours'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))
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