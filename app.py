import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import *
from forms import SignupForm, LoginForm

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
# This method will run before every request that is made.

@app.before_request
def add_user_and_img_path_to_g():
    """Set path to images and if we're logged in, add curr user to Flask global."""
    g.img_path = "/static/images/"

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

##########################################################################
# Global helper functions

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

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