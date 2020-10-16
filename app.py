import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import *
from secrets import *
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
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##########################################################################
# These methods will run before every request that is made.

@app.before_request
def add_to_g():
    """Set path to images, add itinerary (if any), and if we're logged in, add curr user to Flask global."""
    g.img_path = "/static/images/"
    g.prettify_date = prettify_date
    g.prettify_duration = prettify_duration

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
            if new_user.email == email and new_user.username == username and new_user.first_name == first and new_user.last_name == last:
                new_user.is_admin = True
            
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

@app.route('/book', methods=["GET"])
def book_trip():
    if g.user:
        form = BookForm()

        planets = [(p.name, p.name) for p in Planet.query.all()]

        form.planet.choices = planets

        # We have to add all the possible choices for depart_flight, return_flight, and tour here, otherwise WTForms won't
        # recognize the choices that we've populated those fields with on the frontend with JS and will give us errors
        flights = [(f.flight_num, f"Flight: {f.flight_num}") for f in Flight.query.all()]
        form.depart_flight.choices = flights
        form.depart_flight.choices.append((0, "None"))
        form.return_flight.choices = flights
        form.return_flight.choices.append((0, "None"))
        form.tour.choices = [(t.id, t.name) for t in Tour.query.all()]
        form.tour.choices.append((0, "None"))

        # If someone clicks the 'book' button on a particular planet, flight, or tour, I want that planet, or flight or tour's 
        # planet, to be selected
        query_planet = request.args.get('planet', None)
        query_tour = request.args.get('tour', None)
        query_d_flight = request.args.get('d_flight', None)
        query_r_flight = request.args.get('r_flight', None)

        if query_planet:
            planet = Planet.query.get_or_404(query_planet)
            form.planet.data = planet.name

        elif query_tour:
            tour = Tour.query.get_or_404(query_tour)
            form.planet.data = tour.planet_name

        elif query_d_flight:
            flight = Flight.query.get_or_404(query_d_flight)
            form.planet.data = flight.arrive_planet

        elif query_r_flight:
            flight = Flight.query.get_or_404(query_r_flight)
            form.planet.data = flight.depart_planet
            
        # First thing we do is delete the tours, flights, and planets of any unfinished itineraries that we made in previous 
        # visits to our book page (if any)
        if g.itin:
            itin = Itinerary.query.get(g.itin.id)
            itin.start_time = ''
            itin.end_time = ''
            itin.start_date = ''
            itin.end_date = ''
            itin.total = 0
##################################################################################################################################################################################################################
# Still not sure about this part... don't know if deleting the dates deletes them from the itinerary and if so, don't know if I
# can clear an already empty itin.tour_dates/itin.flight_dates.  It may give an error.  Should test in ipython.
            for tour_date in itin.tour_dates:
                db.session.delete(tour_date)

            for flight_date in itin.flight_dates:
                db.session.delete(flight_date)

            itin.tour_dates.clear()
            itin.flight_dates.clear()
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
       
        return render_template('book.html', form=form)
    else:
        flash('Please log in or create an account first!', 'danger')
        return redirect('/')

@app.route('/book/submit', methods=["POST"])
def submit_book_form():
    if g.user:
        form = BookForm()

        planets = [(p.name, p.name) for p in Planet.query.all()]

        form.planet.choices = planets

        # We have to add all the possible choices for depart_flight, return_flight, and tour here, otherwise WTForms won't
        # recognize the choices that we've populated those fields with on the frontend with JS and will give us errors
        flights = [(f.flight_num, f"Flight: {f.flight_num}") for f in Flight.query.all()]
        form.depart_flight.choices = flights
        form.depart_flight.choices.append((0, "None"))
        form.return_flight.choices = flights
        form.return_flight.choices.append((0, "None"))
        form.tour.choices = [(t.id, t.name) for t in Tour.query.all()]
        form.tour.choices.append((0, "None"))

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

            if no_tour and no_depart and no_return:
                flash("You have to select either a flight and flight date or a tour and tour date to submit this form.", "danger")
                return redirect('/book')

            if g.itin and session['itin'] and g.user.id == g.itin.user_id and g.itin.id == session['itin']:                
                itin = Itinerary.query.get(g.itin.id)
                planet = Planet.query.get(planet_name)
                
                itin.planets.append(planet)
                db.session.commit()

                if not no_tour:
                    # If tour_id isn't 0 and tour_date isn't blank, then we get the tour, add the dates to it and commit
                    tour = Tour.query.get(tour_id)
                    tour_dates = TourDate(start_date=tour_date, end_date=set_arrive_end_date(tour_date, tour.start_time, tour.duration), tour_id=tour.id, itinerary_id=itin.id)
                    
                    db.session.add(tour_dates)
                    db.session.commit()

                    if planet_name != tour.planet_name:
                        flash("Your selected planet doesn't match the tour's planet.  Please select the correct planet for the tour.", "danger")
                        return redirect('/book')                

                    # Checks to see if the currently selected flights conflict with one another
                    result1 = compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date, itin)
                    # Checks to see if selected flights' dates and times conflict with the tour start and end date and time
                    result2 = compare_curr_flights_to_curr_tour(no_depart, no_return, depart_id, return_id, depart_date, return_date, tour, itin)
                    # Checks to see if the current tour's start and end datetime conflict with any other tours' start and end datetimes
                    result3 = compare_curr_tour_to_itin_tours(itin, tour)

                    if type(result1) == str:
                        flash(result1, "danger")
                        return redirect('/book')

                    if type(result2) == str:
                        flash(result2, "danger")
                        return redirect('/book')

                    if result3 != "You're all good!":
                        flash(result3, "danger")
                        return redirect('/book')

                    itin.tours.append(tour)
                    itin.total += tour.price
                    db.session.commit()

                    # In cases where we have no flights and only tours or one flight and tours, we need to determine which tour
                    # has the earliest start_date, so it can be the itinerary's start_date, and which tour has the latest
                    # end_date, so it can be the itinerary's end_date
                    start_datetimes = []
                    end_datetimes = []

                    for tour in itin.tours:
                        tour_dates = TourDate.query.filter(TourDate.tour_id == tour.id, TourDate.itinerary_id == itin.id).first()

                        start_datetimes.append(get_datetime(tour_dates.start_date, tour.start_time))
                        end_datetimes.append(get_datetime(tour_dates.end_date, tour.end_time))

                    earliest_datetime = min(start_datetimes)
                    latest_datetime = max(end_datetimes)

                    earliest_datetime_arr = datetime_to_strings(earliest_datetime)
                    latest_datetime_arr = datetime_to_strings(latest_datetime)

                    if len(result2) == 0:
                        itin.start_time = earliest_datetime_arr[0]
                        itin.start_date = earliest_datetime_arr[1]
                        itin.end_time = latest_datetime_arr[0]
                        itin.end_date = latest_datetime_arr[1]

                        db.session.commit()

                    if len(result2) == 1:
                        itin.flights.append(result2[0])
                        db.session.commit()

                        flight_dates = FlightDate.query.filter(FlightDate.flight_num == result2[0].flight_num, FlightDate.itinerary_id == itin.id).first()

                        # If there's only 1 flight, it matters if it's the depart or the return flight.  If it's the depart flight,
                        # then the start time and date for the itinerary will be that flight's start time and date.  If it's the
                        # return flight, then the itinerary's end time and date will be that flight's end time and date.
                        if result2[0].depart_or_return == "depart":
                            itin.start_time = result2[0].depart_time
                            itin.start_date = flight_dates.depart_date
                            itin.end_time = latest_datetime_arr[0]
                            itin.end_date = latest_datetime_arr[1]
                            itin.total += result2[0].price

                            db.session.commit()
                        
                        if result2[0].depart_or_return == "return":
                            itin.start_time = earliest_datetime_arr[0]
                            itin.start_date = earliest_datetime_arr[1]
                            itin.end_time = result2[0].arrive_time
                            itin.end_date = flight_dates.arrive_date
                            itin.total += result2[0].price

                            db.session.commit()

                    if len(result2) == 2:
                        itin.flights.append(result2[0])

                        d_flight_dates = FlightDate.query.filter(FlightDate.flight_num == result2[0].flight_num, FlightDate.itinerary_id == itin.id).first()

                        itin.flights.append(result2[1])

                        r_flight_dates = FlightDate.query.filter(FlightDate.flight_num == result2[1].flight_num, FlightDate.itinerary_id == itin.id).first()

                        itin.start_time = result2[0].depart_time
                        itin.start_date = d_flight_dates.depart_date
                        itin.end_time = result2[1].arrive_time
                        itin.end_date = r_flight_dates.arrive_date

                        itin.total += result2[0].price + result2[1].price

                        db.session.commit()

                    # Compare user's past itineraries to this current one.  If any dates conflict with each other, we flash an 
                    # error
                    resp = compare_curr_itin_to_itins(User.query.get(g.user.id), itin)

                    if resp != "You're all good!":
                        flash(resp, 'danger')
                        return redirect('/book')
                    else:
                        remove_itin()
                        
                        flash("Successfully booked your trip!  Thank you for choosing Star Tours!  Enjoy your trip!", 'success')
                        return render_template('book_success.html', itin=itin)
                else:
                    # If there are no tours
                    result = compare_curr_flights(no_depart, no_return, depart_id, depart_date, return_id, return_date, itin)
                    
                    if type(result) == str:
                        flash(result, 'danger')
                        return redirect('/book')

                    if len(result) == 1:
                        if planet_name != (result[0].depart_planet and result[0].arrive_planet):
                            flash("Your selected planet doesn't match your flight's planet.  Please select the correct planet for flight.", "danger")
                            return redirect('/book')

                        itin.flights.append(result[0])
###################################################################################################################################################################################################
# Left off here
                        itin.start_time = result[0].depart_time
                        itin.start_date = result[0].depart_date
                        itin.end_time = result[0].arrive_time
                        itin.end_date = result[0].arrive_date

                        itin.total += result[0].price

                        db.session.commit()

                    if len(result) == 2:
                        if planet_name != (result[0].depart_planet and result[0].arrive_planet and result[1].depart_planet and result[1].arrive_planet):
                            flash("Your selected planet doesn't match your depart flight's or arrive flight's planets.  Please select the correct planet for the flights.", "danger")
                            return redirect('/book')

                        itin.flights.append(result[0])
                        itin.flights.append(result[1])

                        itin.start_time = result[0].depart_time
                        itin.start_date = result[0].depart_date
                        itin.end_time = result[1].arrive_time
                        itin.end_date = result[1].arrive_date

                        itin.total += result[0].price + result[1].price

                        db.session.commit()

                    resp = compare_curr_itin_to_itins(User.query.get(g.user.id), itin)

                    if resp != "You're all good!":
                        flash(resp, 'danger')
                        return redirect('/book')
                    else:
                        remove_itin()
                        
                        flash("Successfully booked your trip!  Thank you for choosing Star Tours!  Enjoy your trip!", 'success')
                        return render_template('book_success.html', itin=itin)               
            else:
                flash("You have to log in first, then go to the 'Book A Trip' page and click on 'Submit' to access this route.", "danger")
                return redirect('/book')
        else:
            flash("Something went wrong when submitting the form.  Please try again.", "danger")
            return redirect('/book')
    else:
        flash("You have to log in first to access this route.", "danger")
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
    planet = Planet.query.get_or_404(planet_name)

    flights = Flight.query.filter((Flight.depart_planet == planet.name) | (Flight.arrive_planet == planet.name)).all()
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
        planet_name = request.json["planetName"]

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

                if planet_name != tour.planet_name:
                    return (jsonify(msg="Your selected planet doesn't match the tour's planet.  Please select the correct planet for the tour."), 200)                    
                
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
                itin.total += tour.price

                db.session.commit()

                if len(result2) == 0:
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}",
                        "tour_price": f"{tour.price}"
                    }

                    return (jsonify(resp_obj), 200)

                elif len(result2) == 1 and result2[0].depart_or_return == "depart":
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "departure_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "d_flight_price": f"{result2[0].price}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}",
                        "tour_price": f"{tour.price}"   
                    }

                    return (jsonify(resp_obj), 200)

                elif len(result2) == 1 and result2[0].depart_or_return == "return":
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "return_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "return_arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "r_flight_price": f"{result2[0].price}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}",
                        "tour_price": f"{tour.price}"
                    }

                    return (jsonify(resp_obj), 200)

                else:
                    resp_obj = {
                        "msg": "Successfully added tour to user's itinerary.",
                        "departure_datetime": f"{result2[0].depart_time} {result2[0].prettify_depart_date()}",
                        "arrival_datetime": f"{result2[0].arrive_time} {result2[0].prettify_arrive_date()}",
                        "d_flight_price": f"{result2[0].price}",
                        "return_datetime": f"{result2[1].depart_time} {result2[1].prettify_depart_date()}",
                        "return_arrival_datetime": f"{result2[1].arrive_time} {result2[1].prettify_arrive_date()}",
                        "r_flight_price": f"{result2[1].price}",
                        "tour_start_datetime": f"{tour.start_time} {tour.prettify_start_date()}",
                        "tour_end_datetime": f"{tour.end_time} {tour.prettify_end_date()}",
                        "tour_price": f"{tour.price}"                  
                    }

                    return (jsonify(resp_obj), 200)
            else:
                return (jsonify(msg="You must pick a tour and a tour date in order to add another tour."), 200)  
        else:
            return (jsonify(msg="You have to log in first, then go to the 'Book A Trip' page and click on 'Add another planet' to access this route."), 200)
    else:
        return (jsonify(msg="You need to log in first to do that!"), 200)

@app.route('/itineraries/total', methods=["POST"])
def calculate_total():
    """Calculates user's total for trip they're about to book."""
    if g.user and g.itin and g.user.id == g.itin.user_id:
        itin = Itinerary.query.get_or_404(g.itin.id)

        no_depart = request.json["noDepart"]
        no_return = request.json["noReturn"]
        no_tour = request.json["noTour"]
        depart_id = request.json["departId"]
        return_id = request.json["returnId"]
        tour_id = request.json["tourId"]

        total = itin.total

        if not no_depart:
            d_flight = Flight.query.get_or_404(depart_id)
            total += d_flight.price

        if not no_return:
            r_flight = Flight.query.get_or_404(return_id)
            total += r_flight.price

        if not no_tour:
            tour = Tour.query.get_or_404(tour_id)
            total += tour.price

        return (jsonify(total=num_with_commas(str(total))), 200)
    else:
        flash("You have to log in first, go to the 'Book A Trip' page, and click 'Submit' to access this route.", "danger")
        return redirect('/')

##########################################################################
# Delete itinerary route    

@app.route('/itineraries/delete/<int:id>', methods=["POST"])
def delete_itin(id):
    if g.user:
        itin = Itinerary.query.get_or_404(id)

        if g.user.id == itin.user_id:
            db.session.delete(itin)
            db.session.commit()

            flash("Successfully deleted/cancelled trip!", "success")
            return redirect('/account')
        else:
            flash("You don't have authorization to delete that itinerary.", "danger")
            return redirect('/')
    else:
        flash("Please log in first.", "danger")
        return redirect('/')

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

# @app.route('/flights/new', methods=["GET", "POST"])
# def add_new_flight():
#     """Adds a new flight to database, if you're an admin"""
#     form = 

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

##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    return req