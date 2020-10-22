from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

#################################################################################################################################
# HELPER METHODS

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

#################################################################################################################################
# Helper methods for displaying, setting, and comparing dates

def get_tour_start_datetime(tour_date):
    """Pass this function in when sorting itin.tour_dates list.  Will allow us to sort that list by start date/time"""
    datetime_str = f'{tour_date.start_date} {tour_date.tour.start_time}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')

    return datetime_obj
    
def get_flight_depart_datetime(flight_date):
    """Pass this function in when sorting itin.flight_dates list.  Will allow us to sort that list by depart date/time"""
    datetime_str = f'{flight_date.depart_date} {flight_date.flight.depart_time}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')

    return datetime_obj

def get_itin_start_datetime(itin):
    """Pass this function in when sorting itineraries.  Will allow us to sort that list by start date/time"""
    datetime_str = f'{itin.start_date} {itin.start_time}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')

    return datetime_obj

def datetime_to_strings(datetime_obj):
    """Takes a Python datetime object and converts it into 2 strings, one the time and the other the date"""
    time = datetime_obj.strftime("%I:%M %p")
    date = datetime_obj.strftime("%Y-%m-%d")

    return [time, date]

def get_datetime(date, time):
    """Get datetime from flight or tour's time and itinerary's flight or tour date"""
    datetime_str = f'{date} {time}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')

    return datetime_obj

def set_arrive_end_date(depart_start_date, depart_start_time, duration):
    """Takes the flight or tour depart date from the itinerary and flight or tour time and turns them into a datetime object.  
    Then, using the timedelta function, takes the flight or tour time and adds that to the datetime and gives us back a new 
    datetime, whose date we give back as a string."""
    datetime_str = f'{depart_start_date} {depart_start_time}'
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M %p')
    arrive_end_datetime = datetime_obj + timedelta(hours=duration)
    arrive_end_date = arrive_end_datetime.date()

    return arrive_end_date.strftime('%Y-%m-%d')

def prettify_date(date):
    """Displays date as full month name, numbered day, and year"""
    date_as_datetime = datetime.strptime(date, '%Y-%m-%d')
    date_as_date = date_as_datetime.date()
    pretty_date = date_as_date.strftime('%B %-d, %Y')

    return pretty_date

def prettify_duration(duration):
    """Adds 'hour' or 'hours' to the flight/tour time"""
    if duration == 1:
        return f'{duration} hour'
    else:
        return f'{duration} hours'

def compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date, itin, d_flight_dates=None, r_flight_dates=None):
    """Compares current flights to see if they conflict with one another.  Can be especially useful in the /book/submit route when there are only flights booked"""
    if no_depart and no_return:
        return []
    elif no_depart:
        return_flight = Flight.query.get(return_id)
        
        if not r_flight_dates:
            return_flight_dates = FlightDate(depart_date=return_date, arrive_date=set_arrive_end_date(return_date, return_flight.depart_time, return_flight.flight_time), flight_num=return_flight.flight_num, itinerary_id=itin.id)
        
            db.session.add(return_flight_dates)
            db.session.commit()

            return [return_flight, return_flight_dates]
        else:
            return [return_flight, r_flight_dates]
    elif no_return:
        depart_flight = Flight.query.get(depart_id)
        
        if not d_flight_dates:
            depart_flight_dates = FlightDate(depart_date=depart_date, arrive_date=set_arrive_end_date(depart_date, depart_flight.depart_time, depart_flight.flight_time), flight_num=depart_flight.flight_num, itinerary_id=itin.id)
            
            db.session.add(depart_flight_dates)
            db.session.commit()

            return [depart_flight, depart_flight_dates]
        else:
            return [depart_flight, d_flight_dates]

    else:
        depart_flight = Flight.query.get(depart_id)
        
        if not d_flight_dates:
            d_flight_dates = FlightDate(depart_date=depart_date, arrive_date=set_arrive_end_date(depart_date, depart_flight.depart_time, depart_flight.flight_time), flight_num=depart_flight.flight_num, itinerary_id=itin.id)
            
            db.session.add(d_flight_dates)
            db.session.commit()
        
        return_flight = Flight.query.get(return_id)
        
        if not r_flight_dates:
            r_flight_dates = FlightDate(depart_date=return_date, arrive_date=set_arrive_end_date(return_date, return_flight.depart_time, return_flight.flight_time), flight_num=return_flight.flight_num, itinerary_id=itin.id)

            db.session.add(r_flight_dates)
            db.session.commit()

        depart_depart = get_datetime(d_flight_dates.depart_date, depart_flight.depart_time)
        depart_arrive = get_datetime(d_flight_dates.arrive_date, depart_flight.arrive_time)
        return_depart = get_datetime(r_flight_dates.depart_date, return_flight.depart_time)
        return_arrive = get_datetime(r_flight_dates.arrive_date, return_flight.arrive_time)

        if (depart_depart >= return_depart and depart_depart <= return_arrive) or (depart_arrive >= return_depart and depart_arrive <= return_arrive) or (return_depart >= depart_depart and return_depart <= depart_arrive) or (return_arrive >= depart_depart and return_arrive <= depart_arrive):
            return "Your current flights conflict with one another.  Please select a different one."
        else:
            return [depart_flight, d_flight_dates, return_flight, r_flight_dates]

def compare_curr_flights_to_curr_tour(no_depart, no_return, depart_id, return_id, depart_date, return_date, tour, tour_dates, itin, d_flight_dates=None, r_flight_dates=None):
    """Compare current departure and arrival flights' datetimes to current tour's start and end datetimes to see if they conflict."""
    result = compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date, itin, d_flight_dates, r_flight_dates)

    if type(result) == str:
        return result

    elif len(result) == 0:
        return result

    elif len(result) == 2 and result[0].depart_or_return == "depart":
        depart_flight = result[0]
        
        d_flight_dates = result[1]
        
        depart_arrive_datetime = get_datetime(d_flight_dates.arrive_date, depart_flight.arrive_time)
        
        tour_start_datetime = get_datetime(tour_dates.start_date, tour.start_time)
        tour_end_datetime = get_datetime(tour_dates.end_date, tour.end_time)

        if tour_start_datetime <= depart_arrive_datetime or tour_end_datetime <= depart_arrive_datetime:
            return "Your tour needs to start and end after your depart flight's arrival time and date."
        else:
            return [depart_flight, d_flight_dates]

    elif len(result) == 2 and result[0].depart_or_return == "return":
        return_flight = result[0]
        
        r_flight_dates = result[1]

        return_depart_datetime = get_datetime(r_flight_dates.depart_date, return_flight.depart_time)
        
        tour_start_datetime = get_datetime(tour_dates.start_date, tour.start_time)
        tour_end_datetime = get_datetime(tour_dates.end_date, tour.end_time)

        if tour_start_datetime >= return_depart_datetime or tour_end_datetime >= return_depart_datetime:
            return "Your tour needs to start and end before your return flight's depart time and date."
        else:
            return [return_flight, r_flight_dates]

    else:
        depart_flight = result[0]

        d_flight_dates = result[1]
        
        return_flight = result[2]

        r_flight_dates = result[3]

        depart_arrive_datetime = get_datetime(d_flight_dates.arrive_date, depart_flight.arrive_time)
        return_depart_datetime = get_datetime(r_flight_dates.depart_date, return_flight.depart_time)
        
        tour_start_datetime = get_datetime(tour_dates.start_date, tour.start_time)
        tour_end_datetime = get_datetime(tour_dates.end_date, tour.end_time)

        if tour_start_datetime <= depart_arrive_datetime or tour_start_datetime >= return_depart_datetime or tour_end_datetime >= return_depart_datetime or tour_end_datetime <= depart_arrive_datetime:
            return "Your tour needs to start and end after your depart flight's arrival time and date and before your return flight's departure time and date."
        else:
            return [depart_flight, d_flight_dates, return_flight, r_flight_dates]

def compare_curr_tour_to_itin_tours(itin, curr_tour, curr_tour_dates):
    """Compare to see if any of the tour dates and times in the itinerary conflict with the current tour"""        
    curr_tour_start = get_datetime(curr_tour_dates.start_date, curr_tour.start_time)
    curr_tour_end = get_datetime(curr_tour_dates.end_date, curr_tour.end_time)

    if len(itin.tour_dates) > 0:
        for tour_date in itin.tour_dates:
            if curr_tour_dates.id == tour_date.id:
                continue
            
            start = get_datetime(tour_date.start_date, tour_date.tour.start_time)
            end = get_datetime(tour_date.end_date, tour_date.tour.end_time)

            if (curr_tour_start >= start and curr_tour_start <= end) or (curr_tour_end >= start and curr_tour_end <= end) or (start >= curr_tour_start and start <= curr_tour_end) or (end >= curr_tour_start and end <= curr_tour_end):
                return f"This tour's date and time conflicts with a previous tour's date and time - {tour_date.tour.name} at {tour_date.tour.start_time} on {prettify_date(tour_date.start_date)}.  Please choose a different tour or different date."

    return "You're all good!"

def compare_curr_itin_to_itins(user, curr_itin):
    """Compare the start and end datetimes of the user's current itinerary and past itineraries to see if there's any conflicts"""
    itin_start = get_datetime(curr_itin.start_date, curr_itin.start_time)
    itin_end = get_datetime(curr_itin.end_date, curr_itin.end_time)

    if len(user.itineraries) == 0 or (len(user.itineraries) == 1 and user.itineraries[0].id == curr_itin.id):
        return "You're all good!"
    else:
        for itinerary in user.itineraries:
            if itinerary.id == curr_itin.id:
                # continue allows us to skip over all of the code below it and continue on with the for loop.  So, we're basically
                # saying here that if an itinerary in the for loop is the current itinerary, don't compare it, and keep moving on
                # to the next itinerary in the loop
                continue
            itinerary_start = get_datetime(itinerary.start_date, itinerary.start_time)
            itinerary_end = get_datetime(itinerary.end_date, itinerary.end_time)

            if (itin_start >= itinerary_start and itin_start <= itinerary_end) or (itin_end >= itinerary_start and itin_end <= itinerary_end) or (itinerary_start >= itin_start and itinerary_start <= itin_end) or (itinerary_end >= itin_start and itinerary_end <= itin_end):
                return f"Your current trip's start and end time conflicts with your previous trip starting on {prettify_date(itinerary.start_date)} at {itinerary.start_time} and ending on {prettify_date(itinerary.end_date)} at {itinerary.end_time}."

        return "You're all good!"
#################################################################################################################################
# MODELS

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
    depart_or_return = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    flight_time = db.Column(db.Integer, nullable=False)

    dates = db.relationship('FlightDate', backref='flight', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "flight_num": self.flight_num,
            "depart_planet": self.depart_planet,
            "arrive_planet": self.arrive_planet,
            "depart_time": self.depart_time,
            "arrive_time": self.arrive_time,
            "flight_time": prettify_duration(self.flight_time),
            "price": self.price
        }

class Itinerary(db.Model):
    __tablename__ = 'itineraries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.Text)
    end_time = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    total = db.Column(db.Integer, nullable=False, default=0)
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
    tour_dates = db.relationship('TourDate', backref='itinerary', cascade='all, delete-orphan')
    flight_dates = db.relationship('FlightDate', backref='itinerary', cascade='all, delete-orphan')

    def add_commas_to_total(self):
        """Adds commas to large totals making them more clear to read."""
        # This line magically puts commas in the right places for any large number (thousand, million, billion, trillion, etc.)
        return f"{self.total:,d}"

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

class TourDate(db.Model):
    __tablename__ = 'tour_dates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))

class FlightDate(db.Model):
    __tablename__ = 'flight_dates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    depart_date = db.Column(db.Text)
    arrive_date = db.Column(db.Text)
    flight_num = db.Column(db.Integer, db.ForeignKey('flights.flight_num'))
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'))

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
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    planet_name = db.Column(db.Text, db.ForeignKey('planets.name'))

    images = db.relationship('TourImage', backref='tour', cascade='all, delete-orphan')
    dates = db.relationship('TourDate', backref='tour', cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": prettify_duration(self.duration),
            "planet_name": self.planet_name,
            "price": self.price
        }

class TourImage(db.Model):
    __tablename__ = 'tour_images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_name = db.Column(db.Text, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'))