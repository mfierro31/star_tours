from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

def get_gravity(diameter):
    gravity = int(diameter) / 12742
    # This line rounds to exactly 2 decimal places.
    if gravity == 1:
        return f"{round(gravity, 2)} Standard Earth G"
    else:
        return f"{round(gravity, 2)} Standard Earth Gs"

def num_with_commas(num_as_str):
    if num_as_str.isnumeric():
        num_as_int = int(num_as_str)
        # This line magically puts commas in the right places for any large number (thousand, million, billion, trillion, etc.)
        return f"{num_as_int:,d}"
    elif num_as_str.replace('.', '').isnumeric():
        num_as_float = float(num_as_str)
        # This line does the same as the f-string above, but with a float number
        return '{:,.2f}'.format(num_as_float)
    else:
        return num_as_str

def add_km_mi_to_diameter(diameter):
    miles = int(diameter) * 0.62137
    miles_rounded = round(miles, 2)

    return f"{num_with_commas(diameter)} km / {num_with_commas(str(miles_rounded))} mi"

def add_hours_to_rotation(rotation):
    return f"{num_with_commas(rotation)} Earth hours"

def add_days_to_orbit(orbit):
    return f"{num_with_commas(orbit)} Earth days"

def add_percent_to_water(water):
    if water.isnumeric() or water.replace('.', '').isnumeric():
        return f"{water}%"
    else:
        return water

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
    user_email = db.Column(db.Text, db.ForeignKey('users.email'))

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
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

class ItineraryTour(db.Model):
    __tablename__ = 'itineraries_tours'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))

class Planet(db.Model):
    __tablename__ = 'planets'

    name = db.Column(db.Text, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    diameter = db.Column(db.Text, nullable=False)    
    rotation_period = db.Column(db.Text, nullable=False)
    orbital_period = db.Column(db.Text, nullable=False)
    gravity = db.Column(db.Text, nullable=False)
    population = db.Column(db.Text, nullable=False)
    climate = db.Column(db.Text, nullable=False)
    terrain = db.Column(db.Text, nullable=False)
    surface_water = db.Column(db.Text, nullable=False)

    tours = db.relationship('Tour', backref='planet', cascade='all, delete-orphan')
    images = db.relationship('PlanetImage', backref='planet', cascade='all, delete-orphan')

class PlanetImage(db.Model):
    __tablename__ = 'planet_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.Text, nullable=False)
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

    images = db.relationship('TourImage', backref='tour', cascade='all, delete-orphan')

class TourImage(db.Model):
    __tablename__ = 'tour_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.Text, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))