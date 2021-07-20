![Star Tours Logo](Star_Tours_logo.png)

# A travel booking app for Star Wars planets.  Using data taken from the [Star Wars API](https://swapi.dev/).

The Star Tours Travel App (or, just Star Tours, for short) is an app where you can book flights and tours to the most famous Star Wars planets.  You can view it [here](https://star-tours-travel-app.herokuapp.com/).

The app should be quite simple from the user's standpoint.  The main features I've implemented are booking a trip and creating an account.  

Booking is the bread and butter of this app.  This was probably the hardest part to implement because I wanted it to work for a few different scenarios.  I wanted the user to be able to book any amount of tours they wanted (including none) and either 0, 1, or 2 flights, but they still had to book at least one of those things to book a trip.  And none of the flights and tours could conflict with one another either.  I made sure that it's impossible to book a trip where tour and/or flight times overlap with one another, either in the current trip being booked, or in a previously booked trip.  

Creating an account is necessary for the user to book a trip because the trip simply needs to be connected to the user somehow.  That's where the user's account comes in.  I've added standard signup and authentication class methods to the User database model, utilizing bcrypt to hash user passwords.

The standard user flow would be:

1. View planets, tours, flights
2. Create an account or log in
3. Book a trip
4. View booked trips
5. Cancel/delete booked trips (if desired)
6. Edit account info (if desired)
6. Delete account (if desired)

Although [The Star Wars API](https://swapi.dev/) isn't used in any actions a user performs, it was still absolutely essential in building the final product.  I literally cannot even create my database without the information from SWAPI.  I did have a mini heart attack one day when I saw that the SWAPI website was down.  Luckily, another user on GitHub noticed it as well and sent me to [another Star Wars API website](https://swapi-deno.azurewebsites.net/) that had the exact same info as the original one.  Thankfully, as of this commit, the original SWAPI is up and running again.

This project was built with HTML, CSS (Bootstrap), and JavaScript (jQuery) on the front end and Python (Flask) on the back end.  I also used a PostgreSQL database and connected it to Python with Flask-SQLAlchemy as my ORM.

## Running the project

1. After cloning the project to your local machine, set up a virtual environment by running `python3 -m venv venv` in the root directory.  Or, just `python -m venv venv` if you trust your system will point to the correct version of Python.
2. Then, activate that virtual environment with `source venv/bin/activate`.
3. Install all requirements by running `pip3 install -r requirements.txt`, or again, if you trust your machine to point to the right version, `pip install -r requirements.txt`.
4. Then, you'll have to create 2 PostgreSQL databases (if you want to run tests).  Name them `star_tours` and `star-tours-test`.  Read that carefully, one uses an underscore, the other uses dashes.  Yes, bad naming on my part, sorry about that!  Once you have PostgreSQL/psql installed on your machine (you can install it [here](https://www.postgresql.org/download/)), from anywhere in the terminal, you can run the commands - `createdb star_tours` and `createdb star-tours-test` to create these dbs.  When you want to get rid of them, use the `dropdb` command, followed by the db names. 
5. Then, you'll want to seed the `star_tours` db.  We populate the test db when we run the tests.  From the root directory, run `python seed.py`.
4. To run in development mode, set the `FLASK_ENV` to be `development`.  Use the following command to set it up so that you only have to set it once during every new terminal session: `export FLASK_ENV=development`.  Finally, type `flask run`, and voila!  Should be live!
5. I also tested this thing pretty thoroughly too, with the `unittest module`, so to run those... from the root directory, type `python -m unittest`.  I also wrote some doctests in the `models.py` file.  To run those, type `python -m doctest -v models.py`.

### And that's it!  May the force be with you all!

Check me out on [LinkedIn](https://www.linkedin.com/in/mikefie).  I'd love to connect with fellow devs!