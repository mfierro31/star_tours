import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import *

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
    """If we're logged in, add curr user to Flask global."""
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
# Home page route

@app.route('/')
def show_home():
    planets = Planet.query.filter(Planet.name != 'Earth').all()
    return render_template('home.html', planets=planets)

##########################################################################
# Planet routes

@app.route('/planets')
def show_planets():
    planets = Planet.query.filter(Planet.name != 'Earth').all()
    return render_template('planets.html', planets=planets)

@app.route('/planets/<planet_name>')
def show_planet(planet_name):
    planet = Planet.query.get_or_404(planet_name)
    return render_template('planet.html', planet=planet)

##########################################################################
# Tour routes

@app.route('/tours')
def show_tours():
    planets = Planet.query.filter(Planet.name != 'Earth').all()
    return render_template('tours.html', planets=planets)