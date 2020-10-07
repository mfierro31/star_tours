import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import *
from forms import SignupForm, LoginForm, EditUserForm, VerifyUserForm, BookForm
from datetime import datetime

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///star_tours')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##########################################################################
# These methods will run before every request that is made.

@app.before_request
def add_to_g():
    """Set path to images, add itinerary (if any), and if we're logged in, add curr user to Flask global."""
    g.img_path = "/static/images/"

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

    if 'itin' in session:
        g.itin = Itinerary.query.get(session['itin'])

    else:
        g.itin = None

@app.before_request
def make_session_permanent():
    """Sets session to be permanent, so user stays logged in even after quitting out of browser"""
    # Even this has a limit though.  According to Flask docs, the default is 31 days.
    session.permanent = True

##########################################################################
# Global helper functions

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    if 'verified' in session:
        del session['verified']

    if 'itin' in session:
        del session['itin']

def unverify():
    """Unverify a user so that every time they want to change their personal info, the app will ask them to verify their identity"""
    if 'verified' in session:
        del session['verified']

def remove_itin():
    """Remove the user's itinerary from Flask g and from the session"""
    if 'itin' in session:
        del session['itin']

##########################################################################
# User routes

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if g.user:
        flash('Please log out first if you want to create a new account.', 'danger')
        return redirect('/')

    if form.validate_on_submit():
        # Make a list of values from the form.data dict and splat them out into User.signup instead of having to enter
        # every field's data one by one
        form_data = form.data
        form_data.pop('csrf_token')
        form_data = form_data
        form_data = [v for v in form_data.values()]

        new_user = User.signup(*form_data)
        
        if type(new_user) == list:
            # Logic to check the errors.  If it's for both username and email, we want to display both error messages, if just one,
            # we want to display the correct error message for the correct field
            if len(new_user) == 2:
                form.username.errors = [new_user[0]]
                form.email.errors = [new_user[1]]
                # Notice we have to use render_template instead of redirect here, otherwise our errors won't show up
                # This is because with redirect, you can't pass in the form to it.  And since errors are located in form, they
                # don't show up
                return render_template('signup.html', form=form)
            elif 'username' in new_user[0]:
                form.username.errors = [new_user[0]]
                return render_template('signup.html', form=form)
            elif 'email' in new_user[0]:
                form.email.errors = [new_user[0]]
                return render_template('signup.html', form=form)
        else:
            db.session.add(new_user)
            db.session.commit()

            do_login(new_user)

            flash(f'Welcome, {new_user.first_name}!  Successfully created your account!', 'success')
            return redirect('/')
    else:
        return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    if g.user:
        name = g.user.first_name

        do_logout()

        flash(f'Successfully logged out.  Come back soon, {name}!', 'success')
        return redirect('/')
    else:
        flash("You're already logged out!", "danger")
        return redirect('/')

@app.route('/login', methods=["GET", "POST"])
def login():
    if g.user:
        flash("You're already logged in!", "danger")
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        
        if user:
            do_login(user)
            flash(f'Log in successful.  Welcome back, {user.first_name}!', 'success')
            return redirect('/')
        else:
            flash('Incorrect username/password combination.  Please try again.', 'danger')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)

@app.route('/account')
def view_account():
    if g.user:
        return render_template('account.html')
    else:
        flash('Please log in first to view your account.', 'danger')
        return redirect('/')

@app.route('/account/edit/verify', methods=["GET", "POST"])
def verify_user():
    if g.user:
        form = VerifyUserForm()

        if form.validate_on_submit():
            user = User.verify(form.email.data, form.username.data, form.password.data)

            # Check to see if logged in user and verified user are the same user
            if user and user.id == g.user.id:
                session['verified'] = True
                return redirect('/account/edit')
            else:
                flash('Incorrect email, username, and password combination.', 'danger')
                return redirect('/account/edit/verify')
        else:
            return render_template('verify_user.html', form=form)
    else:
        flash('Access denied. Log in first.', 'danger')
        return redirect('/')

@app.route('/account/edit', methods=["GET", "POST"])
def edit_account():
    if 'verified' not in session:
        return redirect('/account/edit/verify')
    
    form = EditUserForm(obj=g.user)

    if g.user:
        user = g.user

        if form.validate_on_submit():
            if form.email.data:
                user.email = form.email.data

            if form.username.data:
                user.username = form.username.data

            if form.password.data:
                user.update_password(form.password.data)

            if form.first_name.data:
                user.first_name = form.first_name.data

            if form.last_name.data:
                user.last_name = form.last_name.data

            db.session.commit()

            unverify()

            flash('Personal info. successfully updated!', 'success')
            return redirect('/account')
        else:
            return render_template('edit_user.html', form=form)
    else:
        flash('Please log in first to edit your account.', 'danger')
        return redirect('/')

##########################################################################
# Book route

@app.route('/book', methods=["GET", "POST"])
def book_trip():
    if g.user:
        form = BookForm()
        
        planets = [(p.name, p.name) for p in Planet.query.all()]

        form.planet.choices = planets
        # First thing we do is delete the tours, flights, and planets of any unfinished itineraries that we made in previous 
        # visits to our book page (if any)
        if g.itin:
            itin = Itinerary.query.get(g.itin.id)
            itin.tours.clear()
            itin.flights.clear()
            itin.planets.clear()

            db.session.commit()
        else:
            # If there isn't an existing itinerary to work from, either because this is the user's first time to the page, or 
            # because a trip was just booked and we cleared session['itin'] and g.itin from the app, we create a new one
            itin = Itinerary(user_id=g.user.id)
            db.session.add(itin)
            db.session.commit()
            # Store this itinerary_id in session so that our itineraries/add/tour and itineraries/add/planet routes can reference
            # it if someone wants to add more tours or planets/flights and so that this newly created itinerary overwrites any
            # previous one(s).  This will also make it so that if we add an extra tour or planet, g.itin will be updated to be this 
            # new itinerary.
            session['itin'] = itin.id

        if form.validate_on_submit():
            tour_id = form.tour.data
            tour_date = form.tour_date.data
            no_tour = form.no_tour.data
            depart_date = form.depart_date.data
            depart_id = form.depart_flight.data
            no_depart = form.no_depart.data
            return_date = form.return_date.data
            return_id = form.return_flight.data
            no_return = form.no_return.data
            planet_name = form.planet.data

            # Checks to see if the currently selected flights conflict with one another
            result1 = compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date)
            # Checks to see if selected flights' dates and times conflict with the tour start and end date and time
            result2 = compare_curr_flights_to_curr_tour(no_depart, no_return, depart_id, return_id, depart_date, return_date, tour)
            # Checks to see if the current tour's start and end datetime conflict with any other tours' start and end datetimes
            result3 = compare_curr_tour_to_itin_tours(itin, tour)

            if type(result1) == str:
                flash(f"{result1}", "danger")
                return redirect('/book')

            if type(result2) == str:
                flash(f"{result2}", "danger")
                return redirect('/book')

            if result3 != "You're all good!":
                flash(f"{result3}", "danger")
                return redirect('/book')

            remove_itin()
            
            flash('Successfully booked your trip!', 'success')
            return redirect('/account')
        else:
            return render_template('book.html', form=form)
    else:
        flash('Please log in or create an account first!', 'danger')
        return redirect('/')

##########################################################################
# API routes for booking form

@app.route('/tours/<planet_name>')
def get_tours(planet_name):
    planet = Planet.query.get_or_404(planet_name)
    tours = planet.tours
    serialized_tours = [tour.serialize() for tour in tours]

    return (jsonify(tours=serialized_tours), 200)

@app.route('/flights/<planet_name>')
def get_flights(planet_name):
    flights = Flight.query.filter((Flight.depart_planet == planet_name) | (Flight.arrive_planet == planet_name)).all()
    flights_serialized = [flight.serialize() for flight in flights]

    return (jsonify(flights=flights_serialized), 200)

@app.route('/itineraries/add/tour', methods=["POST"])
def add_tour_to_itin():
    """Adding a tour to user's itinerary"""
    if g.user:
        tour_id = request.json["tourId"]
        tour_date = request.json["tourDate"]
        no_tour = request.json["noTour"]
        depart_date = request.json["departFlightDate"]
        depart_id = request.json["departFlightId"]
        no_depart = request.json["noDepart"]
        return_date = request.json["returnFlightDate"]
        return_id = request.json["returnFlightId"]
        no_return = request.json["noReturn"]

        if no_tour and no_depart and no_return:
            return (jsonify(msg="You have to select either a flight and date or a tour and date to add another tour."), 200)

        if g.itin and session['itin'] and g.user.id == g.itin.user_id and g.itin.id == session['itin']:                
            itin = Itinerary.query.get(g.itin.id)

            if not no_tour:
                # If tour_id isn't 0 and tour_date isn't blank, then we get the tour, add the dates to it and commit
                tour = Tour.query.get(tour_id)
                tour.start_date = tour_date
                tour.set_end_date()

                db.session.commit()                    
                
                # Checks to see if the currently selected flights conflict with one another
                result1 = compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date)
                # Checks to see if selected flights' dates and times conflict with the tour start and end date and time
                result2 = compare_curr_flights_to_curr_tour(no_depart, no_return, depart_id, return_id, depart_date, return_date, tour)
                # Checks to see if the current tour's start and end datetime conflict with any other tours' start and end datetimes
                result3 = compare_curr_tour_to_itin_tours(itin, tour)

                if type(result1) == str:
                    return (jsonify(msg=result1), 200)

                if type(result2) == str:
                    return (jsonify(msg=result2), 200)

                if result3 != "You're all good!":
                    return (jsonify(msg=result3), 200)

                itin.tours.append(tour)

                db.session.commit()

                if len(result2) == 0:
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}"
                    }

                    return (jsonify(resp_obj), 200)

                elif len(result2) == 1 and result2[0].depart_or_return == "depart":
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "departure_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}"                    
                    }

                    return (jsonify(resp_obj), 200)

                elif len(result2) == 1 and result2[0].depart_or_return == "return":
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "return_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "return_arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}"
                    }

                    return (jsonify(resp_obj), 200)

                else:
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "departure_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "return_datetime": f"{result2[1].depart_time} {result2[1].prettify_depart_date()}",
                        "return_arrival_datetime": f"{result2[1].arrive_time} {result2[1].prettify_arrive_date()}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}"                   
                    }

                    return (jsonify(resp_obj), 200)
            else:
                return (jsonify(msg="You must pick a tour and a tour date in order to add another tour."), 200)  
        else:
            return (jsonify(msg="You have to log in first, then go to the 'Book A Trip' page and click on 'Add another planet' to access this route."), 200)
    else:
        return (jsonify(msg="You need to log in first to do that!"), 200)    

##########################################################################
# Home page route

@app.route('/')
def show_home():
    planets = Planet.query.all()
    return render_template('home.html', planets=planets)

##########################################################################
# Planet routes

@app.route('/planets')
def show_planets():
    planets = Planet.query.all()
    return render_template('planets.html', planets=planets)

@app.route('/planets/<planet_name>')
def show_planet(planet_name):
    planet = Planet.query.get_or_404(planet_name)
    flights = Flight.query.filter((Flight.depart_planet == planet_name) | (Flight.arrive_planet == planet_name)).all()
    return render_template('planet.html', planet=planet, flights=flights)

##########################################################################
# Tour routes

@app.route('/tours')
def show_tours():
    planets = Planet.query.all()
    return render_template('tours.html', planets=planets)

@app.route('/tours/<int:tour_id>')
def show_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template('tour.html', tour=tour)

##########################################################################
# Flight routes

@app.route('/flights')
def show_flights():
    flights = Flight.query.all()
    planets = Planet.query.all()
    return render_template('flights.html', flights=flights, planets=planets)

##########################################################################
# Our Fleet route

@app.route('/fleet')
def show_fleet():
    return render_template('fleet.html')

##########################################################################
# About Us route

@app.route('/about')
def show_about_page():
    return render_template('about.html')