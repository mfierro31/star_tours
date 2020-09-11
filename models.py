from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Helper methods to transform SWAPI data into clearer/cleaner/more logical data

def get_gravity(diameter):
    """Converts SWAPI gravity data into more logical and precise data"""
    gravity = int(diameter) / 12742

    if gravity == 1:
        # This line rounds to exactly 2 decimal places.
        return f"{round(gravity, 2)} Standard Earth G"
    else:
        return f"{round(gravity, 2)} Standard Earth Gs"

def num_with_commas(num_as_str):
    """Adds commas to large numbers making them more clear to read.  If it doesn't convert to a number, it returns num_as_str"""
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
    """Displays the SWAPI diameter data in km and mi"""
    miles = int(diameter) * 0.62137
    miles_rounded = round(miles, 2)

    return f"{num_with_commas(diameter)} km / {num_with_commas(str(miles_rounded))} mi"

def add_hours_to_rotation(rotation):
    """Adds 'Earth hours' to rotation period data from SWAPI"""
    return f"{num_with_commas(rotation)} Earth hours"

def add_days_to_orbit(orbit):
    """Adds 'Earth days' to orbital period data from SWAPI"""
    return f"{num_with_commas(orbit)} Earth days"

def add_percent_to_water(water):
    """Adds a percent sign to the surface water SWAPI data if it's a number"""
    if water.isnumeric() or water.replace('.', '').isnumeric():
        return f"{water}%"
    else:
        return water

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    itinerariess = db.relationship('Itinerary', backref='user', cascade='all, delete-orphan')

    @classmethod
    def signup(cls, email, username, password, first_name, last_name):
        """Creates a user, hashes their password, and adds them to database"""

        # check to see if username and email are unique
        if cls.query.filter_by(username=username).first() and cls.query.filter_by(email=email).first():
            return ["That username has already been taken.  Please choose another one.", "That email already has an account with us.  Please use another."]
        if cls.query.filter_by(username=username).first():
            return ["That username has already been taken.  Please choose another one."]
        if cls.query.filter_by(email=email).first():
            return ["That email already has an account with us.  Please use another."]

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username, password=hashed_pwd, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """
        Checks to see if there is a user with the matching username and password.
        If so, it returns the user, if not, returns False
        """
        user = cls.query.filter_by(username=username).first()

        # If there is a user by that username AND that user's unhashed password matches the password passed in...
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Flight(db.Model):
    __tablename__ = 'flights'

    flight_num = db.Column(db.Integer, primary_key=True)
    depart_planet = db.Column(db.Text, db.ForeignKey('planets.name'))
    arrive_planet = db.Column(db.Text, nullable=False)
    depart_time = db.Column(db.Text, nullable=False)
    arrive_time = db.Column(db.Text, nullable=False)
    depart_date = db.Column(db.Text)
    arrive_date = db.Column(db.Text)
    flight_time = db.Column(db.Integer, nullable=False)

    def prettify_depart_date(self):
        """Takes depart_date as a string, converts it to a datetime object, and displays the date as the full month name, day as
        a number, and year as a number - in that order
        """
        date_as_datetime = datetime.strptime(self.depart_date, '%Y-%m-%d')
        date_as_date = date_as_datetime.date()
        pretty_date = date_as_date.strftime('%B %-d, %Y')

        return pretty_date

    def prettify_arrive_date(self):
        """Does the same thing as prettify_depart_date, except for arrive_date"""
        date_as_datetime = datetime.strptime(self.arrive_date, '%Y-%m-%d')
        date_as_date = date_as_datetime.date()
        pretty_date = date_as_date.strftime('%B %-d, %Y')

        return pretty_date

    def prettify_flight_time(self):
        """Adds 'hour' or 'hours' to the flight time"""
        if self.flight_time == 1:
            return f'{self.flight_time} hour'
        else:
            return f'{self.flight_time} hours'

    def set_arrive_date(self):
        """Takes the depart date and time and turns them into a datetime object.  Then, using the timedelta function, takes the
        flight time and adds that to the depart datetime and gives us back a new datetime, which we set the arrive date to"""
        datetime_str = f'{self.depart_date} {self.depart_time}'
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        arrive_datetime = datetime_obj + timedelta(hours=self.flight_time)
        arrive_date = arrive_datetime.date()

        self.arrive_date = arrive_date.strftime('%Y-%m-%d')

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Should I add any ON DELETE CASCADEs to any of these relationships?  I feel like if I delete any planets, flights, or tours
    # this model won't be affected by that, because these aren't technically columns of data, they're just relationships
    flights = db.relationship('Flight', secondary='itineraries_flights', backref='itineraries')
    planets = db.relationship('Planet', secondary='itineraries_planets', backref='itineraries')
    tours = db.relationship('Tour', secondary='itineraries_tours', backref='itineraries')

class ItineraryFlight(db.Model):
    __tablename__ = 'itineraries_flights'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))
    flight_num = db.Column(db.Integer, db.ForeignKey('flights.flight_num'))

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
    departures = db.relationship('Flight', cascade='all, delete-orphan')

class PlanetImage(db.Model):
    __tablename__ = 'planet_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.Text, nullable=False)
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.Text, nullable=False)
    end_time = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    duration = db.Column(db.Integer, nullable=False)
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

    images = db.relationship('TourImage', backref='tour', cascade='all, delete-orphan')

    # These methods do exactly the same thing as the instance methods in the Flight model do

    def prettify_start_date(self):
        date_as_datetime = datetime.strptime(self.start_date, '%Y-%m-%d')
        date_as_date = date_as_datetime.date()
        pretty_date = date_as_date.strftime('%B %-d, %Y')

        return pretty_date

    def prettify_end_date(self):
        date_as_datetime = datetime.strptime(self.end_date, '%Y-%m-%d')
        date_as_date = date_as_datetime.date()
        pretty_date = date_as_date.strftime('%B %-d, %Y')

        return pretty_date

    def prettify_duration(self):
        if self.duration == 1:
            return f'{self.duration} hour'
        else:
            return f'{self.duration} hours'

    def set_end_date(self):
        datetime_str = f'{self.start_date} {self.start_time}'
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
        end_datetime = datetime_obj + timedelta(hours=self.duration)
        end_date = end_datetime.date()

        self.end_date = end_date.strftime('%Y-%m-%d')

class TourImage(db.Model):
    __tablename__ = 'tour_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.Text, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))