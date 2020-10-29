import os
from unittest import TestCase

from models import *

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database)

os.environ['DATABASE_URL'] = "postgresql:///star-tours-test"

# Now we can import app

from app import app

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data)

db.create_all()

class UserViewTestCase(TestCase):
    """Test view functions related to users"""
    def setUp(self):
        """Create a user"""
        # Have to include these because of the tests below.  This is the correct order to delete everything in without getting
        # any foreign key constraint errors.
        FlightDate.query.delete()
        TourDate.query.delete()

        Flight.query.delete()
        Tour.query.delete()
        Planet.query.delete()

        Itinerary.query.delete()
        User.query.delete()

        self.u = User.signup('test@test.com', 'testy1', 'testing!', 'Testy', 'McTestface')

        db.session.add(self.u)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Remove any fouled transactions"""
        db.session.rollback()

    def test_account_logged_in(self):
        """Can you view your account page if you're logged in?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.get('/account')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p class="text-center">Testy McTestface</p>', html)

    def test_account_logged_out(self):
        """Are you redirected to the home page if you try to view your account page logged out?"""
        resp = self.client.get('/account', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-danger text-center">Please log in first to view your account.</div>', html)

    def test_edit_account_verified(self):
        """Can you edit your account info. without being redirected to the verify page if you're logged in and verified?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['verified'] = True

        resp = self.client.post('/account/edit', data={'first_name': 'Obi-Wan', 'last_name': 'Kenobi'}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p class="text-center">Obi-Wan Kenobi</p>', html)
        self.assertIn('<div class="alert alert-success text-center">Personal info. successfully updated!</div>', html)

    def test_edit_account_unverified(self):
        """Do you get redirected to the verify page if you try to edit your account but you're not verified?"""
        # Logged in, but not verified
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.post('/account/edit', data={'first_name': 'Obi-Wan', 'last_name': 'Kenobi'}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<p class="text-center text-md-left">As an added layer of protection, please verify your credentials first before editing your personal information.</p>', html)

    def test_delete_account_logged_in(self):
        """Can you successfully delete your account while logged in?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.post('/user/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-success text-center">Successfully deleted your account!</div>', html)

    def test_delete_account_logged_out(self):
        """Do you get redirected to home page with an error message when you try to delete your account logged out?"""
        resp = self.client.post('/user/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-danger text-center">You need to log in first to access this route.</div>', html)

class TripViewTestCase(TestCase):
    """Test view functions related to trips/itineraries"""

    def setUp(self):
        """Create a user, planet, flights, and tours"""
        FlightDate.query.delete()
        TourDate.query.delete()

        Flight.query.delete()
        Tour.query.delete()
        Planet.query.delete()

        Itinerary.query.delete()
        User.query.delete()

        db.session.commit()

        self.u = User.signup('test@test.com', 'testy1', 'testing!', 'Testy', 'McTestface')
        db.session.add(self.u)
        db.session.commit()

        self.i = Itinerary(user_id=self.u.id)
        db.session.add(self.i)
        db.session.commit()

        self.p = Planet(name="Naboo", description="Eh...", diameter="Eh", rotation_period="Eh", orbital_period="Eh", gravity="Eh", population="Eh", climate="Eh", terrain="Eh", surface_water="Eh")
        db.session.add(self.p)
        db.session.commit()

        self.f1 = Flight(flight_num=5700, depart_planet="Earth", arrive_planet="Naboo", depart_time="07:00 PM", arrive_time="07:00 AM", depart_or_return="depart", price=250, flight_time=12)
        self.f2 = Flight(flight_num=5701, depart_planet="Naboo", arrive_planet="Earth", depart_time="12:30 PM", arrive_time="12:30 AM", depart_or_return="return", price=250, flight_time=12)

        self.t1 = Tour(name="TestTour1", description="blablabla", start_time="12:00 PM", end_time="03:00 PM", duration=3, price=45, planet_name="Naboo")
        self.t2 = Tour(name="TestTour2", description="blablabla-dadadadada", start_time="03:30 PM", end_time="06:30 PM", duration=3, price=60, planet_name="Naboo")

        db.session.add_all([self.f1, self.f2, self.t1, self.t2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Remove any fouled transactions"""
        db.session.rollback()

    def test_book_page_logged_in(self):
        """Are you able to see the booking page if you're logged in?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.get('/book')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)

    def test_book_page_logged_out(self):
        """Are you redirected to the signup page if you try to view the book page and you're logged out?"""
        resp = self.client.get('/book', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-danger text-center">Please log in or create an account first!</div>', html)
        self.assertIn('<h1 class="display-1 text-center text-warning long-text">Create An Account</h1>', html)

    def test_book_with_query_params(self):
        """If there are query strings in the url, does the view function select the correct planet?"""

    def test_book_with_itin(self):
        """If there's already an itin in session, will the view function reset all its values?"""

    def test_book_without_itin(self):
        """If there is no itin in session, will the view function create a blank one for us?"""

    def test_book_submit_logged_out(self):
        """Will we be redirected to home page if we try to submit our trip, but we're not logged in?"""

    def test_book_submit_without_itin(self):
        """Will we be redirected to book page if we try to submit a trip with no itin in session?"""

    def test_book_many_flights_many_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 2 flights?"""

    def test_book_many_flights_one_tour(self):
        """Will we be successfully routed to the correct version of the book success page if we book 1 tour and 2 flights?"""

    def test_book_many_flights_no_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book 0 tours and 2 flights?"""

    def test_book_many_tours_one_flight(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 1 flight?"""

    def test_book_many_tours_no_flights(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 0 flights?"""

    def test_book_no_tours_no_flights_but_itin_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book no tours and no flights, but still have tours in our current itinerary?"""

    def test_book_no_tours_no_flights(self):
        """Will we be successfully redirected back to the book page if we book no tours and no flights?"""