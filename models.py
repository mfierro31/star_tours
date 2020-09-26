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

# Helper method for comparing dates

def strings_to_datetime(date_str, time_str):
    """Convert a date and time string - formatted as '2020-09-30' and '09:00 AM' - into a datetime object"""
    datetime_str = f'{date_str} {time_str}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')

    return datetime_obj

def compare_flight_dates_to_tour_dates(depart_flight_id, return_flight_id, depart_flight_date, return_flight_date, tour):
    """Compare departure and arrival flights' datetimes to tour's start and end datetimes to see if they conflict"""
    if depart_flight_id and return_flight_id and depart_flight_date and return_flight_date:
        depart_flight = Flight.query.get(depart_flight_id)
        depart_flight.depart_date = depart_flight_date
        depart_flight.set_arrive_date()

        return_flight = Flight.query.get(return_flight_id)
        return_flight.depart_date = return_flight_date
        return_flight.set_arrive_date()
        
        db.session.commit()

        depart_arrive_datetime = strings_to_datetime(depart_flight.arrive_date, depart_flight.arrive_time)
        return_depart_datetime = strings_to_datetime(return_flight.depart_date, return_flight.depart_time)

        tour_start_datetime = strings_to_datetime(tour.start_date, tour.start_time)
        tour_end_datetime = strings_to_datetime(tour.end_date, tour.end_time)

        if tour_start_datetime < depart_arrive_datetime or tour_start_datetime > return_depart_datetime or tour_end_datetime > return_depart_datetime or tour_end_datetime < depart_arrive_datetime:
            return "Your tour needs to start and end after your arrival time and date and before your departure time and date."
        else:
            return "You're all good!"

    elif depart_flight_id and depart_flight_date:
        depart_flight = Flight.query.get(depart_flight_id)
        depart_flight.depart_date = depart_flight_date
        depart_flight.set_arrive_date()
        
        db.session.commit()

        depart_arrive_datetime = strings_to_datetime(depart_flight.arrive_date, depart_flight.arrive_time)

        tour_start_datetime = strings_to_datetime(tour.start_date, tour.start_time)
        tour_end_datetime = strings_to_datetime(tour.end_date, tour.end_time)

        if tour_start_datetime < depart_arrive_datetime or tour_end_datetime < depart_arrive_datetime:
            return "Your tour needs to start and end after your arrival time and date."
        else:
            return "You're all good!"

    elif not depart_flight_id and not return_flight_id and not depart_flight_date and not return_flight_date:
        return "You're all good!"

    else:
        return "If you're going to book a flight, make sure to pick both a date and a flight.  If you're not, then make sure to clear both date fields and select 'None' for both flights."

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    itineraries = db.relationship('Itinerary', backref='user', cascade='all, delete-orphan')

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

    @classmethod
    def verify(cls, email, username, password):
        """Verifies the identity of the user when user tries to change their personal information"""
        user = cls.query.filter(cls.email == email, cls.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    def update_password(self, password):
        """Sets user's password to a new hashed password"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf8')
        self.password = hashed_pwd

class Flight(db.Model):
    __tablename__ = 'flights'

    flight_num = db.Column(db.Integer, primary_key=True)
    depart_planet = db.Column(db.Text, nullable=False)
    arrive_planet = db.Column(db.Text, nullable=False)
    depart_time = db.Column(db.Text, nullable=False)
    arrive_time = db.Column(db.Text, nullable=False)
    depart_date = db.Column(db.Text)
    arrive_date = db.Column(db.Text)
    flight_time = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "num": self.flight_num,
            "depart_planet": self.depart_planet,
            "arrive_planet": self.arrive_planet,
            "depart_time": self.depart_time,
            "arrive_time": self.arrive_time,
            "depart_date": self.depart_date,
            "arrive_date": self.arrive_date,
            "flight_time": self.prettify_flight_time()
        }

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

    def get_depart_datetime(self):
        """Returns datetime object using the flight's depart time and date"""
        depart_datetime_str = f'{self.depart_date} {self.depart_time}'
        depart_datetime_obj = datetime.strptime(depart_datetime_str, '%Y-%m-%d %I:%M %p')

        return depart_datetime_obj

    def get_arrive_datetime(self):
        """Returns datetime object using the flight's arrive time and date"""
        arrive_datetime_str = f'{self.arrive_date} {self.arrive_time}'
        arrive_datetime_obj = datetime.strptime(arrive_datetime_str, '%Y-%m-%d %I:%M %p')

        return arrive_datetime_obj

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Be careful with deleting individual items in these relationships - you could potentially delete the items in these 
    # relationships not just from the relationship itself, but also from the entire database.  So instead of using
    # db.session.delete(me.itineraries[0].flights[0]), which will delete the item from the entire database, use methods 
    # associated with the relationship, like .remove(), which will remove whatever object you pass in - EXAMPLE:

        # me.itineraries[0].flights.remove(Flight.query.get(5701))

    # Or there is also a .pop() method that removes and returns the item at the index you pass in.  If you don't pass in an
    # index, it will remove and return the last item in the relationship list.  EXAMPLE:

        # me.itineraries[0].flights.pop(0)
        # ---> <Flight 5700>
        # me.itineraries[0].flights
        # ---> [<Flight 5701>]

    # There are other useful methods for relationships.  Just go into ipython and pass in me.itineraries[0].flights to the help()
    # method.

    flights = db.relationship('Flight', secondary="itineraries_flights", backref='itineraries')
    planets = db.relationship('Planet', secondary="itineraries_planets", backref='itineraries')
    tours = db.relationship('Tour', secondary="itineraries_tours", backref='itineraries')

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

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "duration": self.prettify_duration(),
            "planet_name": self.planet_name
        }

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