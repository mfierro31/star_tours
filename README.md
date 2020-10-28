![Star Tours Logo](Star_Tours_logo.png)

# A mock travel site for Star Wars planets.  Using data taken from the [Star Wars API](https://swapi.dev/).

The Star Tours Travel App is an app where you can book flights and tours to the most famous Star Wars planets.  You can view it [here](https://star-tours-travel-app.herokuapp.com/).

The app is quite simple from the user's standpoint.  The main features I've implemented are booking a trip and creating an account.  

Booking is obviously the bread and butter of this app.  This was probably the hardest part to implement because I wanted it to work for a few different scenarios.  I wanted the user to be able to book either 1 or 2 flights and as many tours as they wanted, no flights and as many tours as they wanted, no tours and either 1 or 2 flights, and if the user clicked 'add another tour', but then selected the 'no tour' option or 'none', they could still book their previous tour(s).

Creating an account is necessary for the user to book a trip because the trip simply needs to be connected to the user somehow.  That's where the user's account comes in.  I've added standard signup and authentication class methods to the User model utilizing bcrypt to hash user passwords.

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