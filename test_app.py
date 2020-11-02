import os
from unittest import TestCase
from datetime import date
from flask import session

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
        ItineraryFlight.query.delete()
        ItineraryTour.query.delete()
        ItineraryPlanet.query.delete()

        PlanetImage.query.delete()
        TourImage.query.delete()

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

class BookingViewTestCase(TestCase):
    """Test view functions related to booking a trip"""

    def setUp(self):
        """Create a user, planet, flights, and tours"""
        ItineraryFlight.query.delete()
        ItineraryTour.query.delete()
        ItineraryPlanet.query.delete()

        PlanetImage.query.delete()
        TourImage.query.delete()

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

        # Have to add images to planets and tours, otherwise we'll get errors in our responses
        self.p = Planet(name="Naboo", description="Eh...", diameter="Eh", rotation_period="Eh", orbital_period="Eh", gravity="Eh", population="Eh", climate="Eh", terrain="Eh", surface_water="Eh")
        self.pi1 = PlanetImage(image_name="Naboo.png", planet_name="Naboo")
        self.pi2 = PlanetImage(image_name="Naboo_palace.jpg", planet_name="Naboo")

        db.session.add_all([self.p, self.pi1, self.pi2])
        db.session.commit()

        self.f1 = Flight(flight_num=5700, depart_planet="Earth", arrive_planet="Naboo", depart_time="07:00 PM", arrive_time="07:00 AM", depart_or_return="depart", price=250, flight_time=12)
        self.f2 = Flight(flight_num=5701, depart_planet="Naboo", arrive_planet="Earth", depart_time="07:00 PM", arrive_time="07:00 AM", depart_or_return="return", price=250, flight_time=12)

        self.t1 = Tour(name="TestTour1", description="blablabla", start_time="12:00 PM", end_time="03:00 PM", duration=3, price=45, planet_name="Naboo")
        self.t2 = Tour(name="TestTour2", description="blablabla-dadadadada", start_time="12:00 PM", end_time="03:00 PM", duration=3, price=60, planet_name="Naboo")

        db.session.add_all([self.f1, self.f2, self.t1, self.t2])
        db.session.commit()

        self.ti1 = TourImage(image_name="Naboo_palace.jpg", tour_id=self.t1.id)
        self.ti2 = TourImage(image_name="Naboo_tribubble_bongo.jpeg", tour_id=self.t2.id)

        db.session.add_all([self.ti1, self.ti2])
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
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.get('/book?d_flight=5700')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<option selected value="Naboo">Naboo</option>', html)

    def test_book_with_itin(self):
        """If there's already an itin in session, will the view function reset all its values?"""
        self.i.start_time = "09:00 AM"
        self.i.end_time = "05:00 PM"
        self.i.start_date = "2020-11-01"
        self.i.end_date = "2020-11-09"
        self.i.total = 605

        self.i.planets.append(self.p)
        self.i.flights.append(self.f1)
        self.i.flights.append(self.f2)
        self.i.tours.append(self.t1)
        self.i.tours.append(self.t2)

        db.session.commit()

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.get('/book')

        itin = Itinerary.query.get(session['itin'])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(itin.start_time, '')
        self.assertEqual(itin.end_time, '')
        self.assertEqual(itin.start_date, '')
        self.assertEqual(itin.end_date, '')
        self.assertEqual(itin.total, 0)
        self.assertEqual(len(itin.planets), 0)
        self.assertEqual(len(itin.tours), 0)
        self.assertEqual(len(itin.flights), 0)

    def test_book_without_itin(self):
        """If there is no itin in session, will the view function create a blank one for us?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.get('/book')

        itins = Itinerary.query.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(itins), 2)

    def test_book_submit_logged_out(self):
        """Will we be redirected to home page if we try to submit our trip, but we're not logged in?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-danger text-center">You have to log in first to access this route.</div>', html)
        self.assertIn('<h1 class="text-center">Light speed to your favorite destinations across the galaxy!</h1>', html)

    def test_book_submit_without_itin(self):
        """Will we be redirected to book page if we try to submit a trip with no itin in session?"""
        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<div class="alert alert-danger text-center">You have to log in first, then go to the &#39;Book A Trip&#39; page and click on &#39;Submit&#39; to access this route.</div>', html)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)

    def test_book_submit_many_flights_many_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 2 flights?"""
        self.i.tours.append(self.t1)
    
        t1_date = TourDate(start_date='2020-11-10', end_date='2020-11-10', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        # Must format the form values like this:
        # {'depart_date': datetime.date(2020, 11, 9), 'return_date': None, 'planet': 'Tatooine', 'depart_flight': 5824, 'return_flight': 0, 'tour': 1, 'tour_date': datetime.date(2020, 11, 11), 'no_depart': False, 'no_return': True, 'no_tour': False}
        
        # literally writing datetime.date for the dates will result in an error.  The easiest way to get around this is to import
        # only date from datetime and use just date instead

        # Also, a weird quirk of Boolean Fields in WTForms... if you set the value of a Boolean Field as False, it will consider
        # that to actually be a True value.  So instead of literally writing False, we can write '' and that will translate to 
        # False

        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 12),
            'no_tour': '',
            'depart_date': date(2020, 11, 7),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': date(2020, 11, 14),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as change_session:
            change_session['curr_user'] = self.u.id
            change_session['itin'] = self.i.id

        # Wanted to test that 'itin' was deleted from session here, so I had to move all of the assert statements below into a
        # with block, otherwise we'd get an error testing the session saying that we're working outside of request context.
        with self.client as client:
            resp = self.client.post('/book/submit', data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('itin', session)
            self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Get ready, Testy, you\'re going to...</h1>', html)
            self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text"><b><i>Naboo!!!</i></b></h1>', html)
            self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Looks like you booked some awesome tours too!</h3>', html)
            self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tours and flights, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your trip!</h5>', html)

    def test_book_submit_many_flights_one_tour(self):
        """Will we be successfully routed to the correct version of the book success page if we book 1 tour and 2 flights?"""    
        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 12),
            'no_tour': '',
            'depart_date': date(2020, 11, 7),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': date(2020, 11, 14),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Get ready, Testy, you\'re going to...</h1>', html)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text"><b><i>Naboo!!!</i></b></h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Looks like you booked an awesome tour too!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tour and flights, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your trip!</h5>', html)

    def test_book_submit_many_flights_no_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book 0 tours and 2 flights?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': date(2020, 11, 7),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': date(2020, 11, 14),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Get ready, Testy, you\'re going to...</h1>', html)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text"><b><i>Naboo!!!</i></b></h1>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the flights, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your trip!</h5>', html)

    def test_book_submit_no_tours_depart_flight(self):
        """Will we be successfully routed to the correct version of the book success page if we book 0 tours and a depart flight?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': date(2020, 11, 7),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Get ready, Testy, you\'re going to...</h1>', html)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text"><b><i>Naboo!!!</i></b></h1>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the flight, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your trip!</h5>', html)

    def test_book_submit_no_tours_return_flight(self):
        """Will we be successfully routed to the correct version of the book success page if we book 0 tours and a return flight?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': date(2020, 11, 14),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Hey, Testy!  Looks like you\'re headed home.</h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Hope you enjoyed your time on Naboo!  Welcome back to Earth!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the flight, or any last pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  Enjoy your flight!</h5>', html)

    def test_book_submit_many_tours_one_flight(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 1 flight?"""
        self.i.tours.append(self.t1)
    
        t1_date = TourDate(start_date='2020-11-10', end_date='2020-11-10', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 12),
            'no_tour': '',
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': date(2020, 11, 14),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Hey, Testy!  Looks like you\'re headed home.</h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">But not before getting some last-minute tours in!  Enjoy!  And welcome back to Earth!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tours or flight, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your last tours and flight!', html)

    def test_book_submit_many_tours_no_flights(self):
        """Will we be successfully routed to the correct version of the book success page if we book 2 tours and 0 flights?"""
        self.i.tours.append(self.t1)
    
        t1_date = TourDate(start_date='2020-11-10', end_date='2020-11-10', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 12),
            'no_tour': '',
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Hey, Testy!  Hope you\'re enjoying your time on Naboo!</h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Looks like you booked some new tours on-planet.  Enjoy!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tours, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your tours!</h5>', html)

    def test_book_submit_one_tour_no_flights(self):
        """Will we be successfully routed to the correct version of the book success page if we book 1 tour and 0 flights?"""
        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 12),
            'no_tour': '',
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Hey, Testy!  Hope you\'re enjoying your time on Naboo!</h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Looks like you booked a new tour on-planet.  Enjoy!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tour, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your tour!</h5>', html)

    def test_book_submit_no_tours_no_flights_but_itin_tours(self):
        """Will we be successfully routed to the correct version of the book success page if we book no tours and no flights, but still have tours in our current itinerary?"""
        self.i.tours.append(self.t1)
    
        t1_date = TourDate(start_date='2020-11-10', end_date='2020-11-10', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center text-warning display-1 mb-5 long-text">Hey, Testy!  Hope you\'re enjoying your time on Naboo!</h1>', html)
        self.assertIn('<h3 class="text-center text-warning display-3 mb-5 long-text-sub">Looks like you booked a new tour on-planet.  Enjoy!</h3>', html)
        self.assertIn('<h5 class="text-center mb-5">Spread the word about us!  Share this screenshot and/or your pics from the tour, or any pics you take on-planet, on social media with the hashtag <span class="text-primary">#StarTours</span>.  It would help us out a lot.  Thanks, Testy!  And enjoy your tour!</h5>', html)
       
    def test_book_submit_no_tours_no_flights(self):
        """Will we be successfully redirected back to the book page if we book no tours and no flights?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">You have to select either a flight and flight date or a tour and tour date to submit this form.</div>', html)

    def test_book_submit_flights_conflict(self):
        """Will we be redirected back to book page if the flight dates conflict with each other?"""
        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': date(2020, 11, 10),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': date(2020, 11, 10),
            'return_flight': 5701,
            'no_return': '',
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">Your current flights conflict with one another.  Please select a different one.</div>', html)

    # This test below doubles as a flight conflicts with tour in itinerary test as well, because every time a user adds a new
    # tour, they're being compared against the same flight(s) every time.

    def test_book_submit_flight_conflicts_with_tour(self):
        """Will we be redirected back to book page if a flight conflicts with the current tour?"""
        data = {
            'tour': self.t1.id,
            'tour_date': date(2020, 11, 10),
            'no_tour': '',
            'depart_date': date(2020, 11, 10),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">Your tour needs to start and end after your depart flight&#39;s arrival time and date.</div>', html)

    def test_book_submit_tour_conflicts_with_itin_tour(self):
        """Will we be redirected back to book page if the current tour's date conflicts with a tour date in the current itinerary?"""
        self.i.tours.append(self.t1)
    
        t1_date = TourDate(start_date='2020-11-10', end_date='2020-11-10', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        data = {
            'tour': self.t2.id,
            'tour_date': date(2020, 11, 10),
            'no_tour': '',
            'depart_date': None,
            'depart_flight': 0,
            'no_depart': True,
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">This tour&#39;s date and time conflicts with a previous tour&#39;s date and time - TestTour1 at 12:00 PM on November 10, 2020.  Please choose a different tour or different date.</div>', html)

    def test_book_submit_itins_conflict(self):
        """Will we be redirected back to the book page if the current itinerary conflicts with another itinerary?"""
        new_itin = Itinerary(user_id=self.u.id, start_time="07:00 PM", end_time="07:00 AM", start_date="2020-11-10", end_date="2020-11-11")

        db.session.add(new_itin)
        db.session.commit()

        data = {
            'tour': 0,
            'tour_date': None,
            'no_tour': True,
            'depart_date': date(2020, 11, 10),
            'depart_flight': 5700,
            'no_depart': '',
            'return_date': None,
            'return_flight': 0,
            'no_return': True,
            'planet': 'Naboo'
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/book/submit', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1 text-center text-warning mb-4 long-text">Book A Trip</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">Your current trip&#39;s start and end time conflicts with your previous trip starting on November 10, 2020 at 07:00 PM and ending on November 11, 2020 at 07:00 AM.</div>', html)

class ItineraryViewTestCase(TestCase):
    """Testing the view functions and API routes related to itineraries"""

    def setUp(self):
        """Create a user and itinerary"""
        ItineraryFlight.query.delete()
        ItineraryTour.query.delete()
        ItineraryPlanet.query.delete()

        PlanetImage.query.delete()
        TourImage.query.delete()

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

        self.i = Itinerary(user_id=self.u.id)

        db.session.add(self.i)
        db.session.commit()

        self.f1 = Flight(flight_num=5700, depart_planet="Earth", arrive_planet="Naboo", depart_time="07:00 PM", arrive_time="07:00 AM", depart_or_return="depart", price=250, flight_time=12)
        self.f2 = Flight(flight_num=5701, depart_planet="Naboo", arrive_planet="Earth", depart_time="07:00 PM", arrive_time="07:00 AM", depart_or_return="return", price=250, flight_time=12)

        self.p = Planet(name="Naboo", description="Eh...", diameter="Eh", rotation_period="Eh", orbital_period="Eh", gravity="Eh", population="Eh", climate="Eh", terrain="Eh", surface_water="Eh")
        self.pi = PlanetImage(image_name="Naboo.png", planet_name="Naboo")
        
        db.session.add_all([self.p, self.pi])
        db.session.commit()

        self.t1 = Tour(name="TestTour1", description="blablabla", start_time="12:00 PM", end_time="03:00 PM", duration=3, price=45, planet_name="Naboo")
        self.t2 = Tour(name="TestTour2", description="blablabla-dadadadada", start_time="12:00 PM", end_time="03:00 PM", duration=3, price=60, planet_name="Naboo")

        db.session.add_all([self.f1, self.f2, self.t1, self.t2])
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Remove any fouled transactions"""
        db.session.rollback()

    def test_add_tour_logged_out(self):
        """Do we get correct JSON response if we try to access this route while logged out?"""
        json_dict = {
            "tourId": 0,
            "tourDate": None,
            "noTour": True,
            "departFlightDate": None,
            "departFlightId": 0,
            "noDepart": True,
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"msg": "You need to log in first to do that!"})

    def test_add_tour_with_no_itin(self):
        """Do we get correct JSON response if we try to access this route while logged in, but with no itin in session?"""
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": date(2020, 11, 10),
            "noTour": '',
            "departFlightDate": None,
            "departFlightId": 0,
            "noDepart": True,
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"msg": "You have to log in first, then go to the 'Book A Trip' page and click on 'Add another tour' to access this route."})

    def test_add_tour_no_tour_selected(self):
        """Do we get correct JSON response if we try to access this route with no tour selected?"""
        json_dict = {
            "tourId": 0,
            "tourDate": None,
            "noTour": True,
            "departFlightDate": date(2020, 11, 10),
            "departFlightId": 5700,
            "noDepart": '',
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"msg": "You must pick a tour and a tour date in order to add another tour."})

    def test_add_tour_flight_conflicts_with_tour(self):
        """Do we get correct JSON response if we select a date for our current tour that conflicts with one of our current flights?"""
        # Have to set the dates as strings now, otherwise our functions will fail, because using date() converts it into the wrong 
        # format
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": '2020-11-10',
            "noTour": '',
            "departFlightDate": '2020-11-10',
            "departFlightId": 5700,
            "noDepart": '',
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"msg": "Your tour needs to start and end after your depart flight's arrival time and date."})
        # Also check to see if the newly created tour_date object is deleted, both from the database and from itin.tour_dates
        # Have to create a new instance of our current itinerary, otherwise we'll get a lazy load error when trying to access
        # self.i.tour_dates
        itin = Itinerary.query.get(self.i.id)
        self.assertEqual(len(itin.tour_dates), 0)
        self.assertEqual(TourDate.query.count(), 0)

    def test_add_tour_curr_tour_conflicts_with_itin_tour(self):
        """Do we get correct JSON response if we select a date for our current tour that conflicts with one of the tour dates in our itinerary?"""
        self.i.tours.append(self.t1)

        t1_date = TourDate(start_date='2020-11-13', end_date='2020-11-13', tour_id=self.t1.id, itinerary_id=self.i.id)

        db.session.add(t1_date)
        db.session.commit()

        json_dict = {
            "tourId": self.t2.id,
            "tourDate": '2020-11-13',
            "noTour": '',
            "departFlightDate": '2020-11-10',
            "departFlightId": 5700,
            "noDepart": '',
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"msg": "This tour's date and time conflicts with a previous tour's date and time - TestTour1 at 12:00 PM on November 13, 2020.  Please choose a different tour or different date."})
        # Also check to see if our current tour's tour_date object is deleted, both from the database and from itin.tour_dates
        itin = Itinerary.query.get(self.i.id)
        # In this situation, we'll still have 1 tour date, the one we created at the top of this test
        self.assertEqual(len(itin.tour_dates), 1)
        self.assertEqual(TourDate.query.count(), 1)

    def test_add_tour_no_flights(self):
        """Do we get correct JSON response if we successfully add a tour with no flights?"""
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": '2020-11-10',
            "noTour": '',
            "departFlightDate": None,
            "departFlightId": 0,
            "noDepart": True,
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        json_resp = {
            "msg": "Successfully added tour to user's itinerary.",
            "tour_start_datetime": "12:00 PM November 10, 2020",
            "tour_end_datetime": "03:00 PM November 10, 2020",
            "tour_price": "45"
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, json_resp)

    def test_add_tour_depart_flight(self):
        """Do we get correct JSON response if we successfully add a tour with only one (depart) flight?"""
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": '2020-11-12',
            "noTour": '',
            "departFlightDate": '2020-11-10',
            "departFlightId": 5700,
            "noDepart": '',
            "returnFlightDate": None,
            "returnFlightId": 0,
            "noReturn": True,
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        json_resp = {
            "msg": "Successfully added tour to user's itinerary.",
            "departure_datetime": "07:00 PM November 10, 2020",
            "arrival_datetime": "07:00 AM November 11, 2020",
            "d_flight_price": "250",
            "tour_start_datetime": "12:00 PM November 12, 2020",
            "tour_end_datetime": "03:00 PM November 12, 2020",
            "tour_price": "45"
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, json_resp)        

    def test_add_tour_return_flight(self):
        """Do we get correct JSON response if we successfully add a tour with only one (return) flight?"""
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": '2020-11-12',
            "noTour": '',
            "departFlightDate": None,
            "departFlightId": 0,
            "noDepart": True,
            "returnFlightDate": '2020-11-14',
            "returnFlightId": 5701,
            "noReturn": '',
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        json_resp = {
            "msg": "Successfully added tour to user's itinerary.",
            "return_datetime": "07:00 PM November 14, 2020",
            "return_arrival_datetime": "07:00 AM November 15, 2020",
            "r_flight_price": "250",
            "tour_start_datetime": "12:00 PM November 12, 2020",
            "tour_end_datetime": "03:00 PM November 12, 2020",
            "tour_price": "45"
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, json_resp)

    def test_add_tour_two_flights(self):
        """Do we get correct JSON response if we successfully add a tour with two flights?"""
        json_dict = {
            "tourId": self.t1.id,
            "tourDate": '2020-11-12',
            "noTour": '',
            "departFlightDate": '2020-11-10',
            "departFlightId": 5700,
            "noDepart": '',
            "returnFlightDate": '2020-11-14',
            "returnFlightId": 5701,
            "noReturn": '',
            "planetName": "Naboo"
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/add/tour', json=json_dict)

        json_resp = {
            "msg": "Successfully added tour to user's itinerary.",
            "departure_datetime": "07:00 PM November 10, 2020",
            "arrival_datetime": "07:00 AM November 11, 2020",
            "d_flight_price": "250",
            "return_datetime": "07:00 PM November 14, 2020",
            "return_arrival_datetime": "07:00 AM November 15, 2020",
            "r_flight_price": "250",
            "tour_start_datetime": "12:00 PM November 12, 2020",
            "tour_end_datetime": "03:00 PM November 12, 2020",
            "tour_price": "45"
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, json_resp)

    def test_total_logged_out_no_itin(self):
        """Do we get redirected to the home page if we try to access this route logged out and with no itin in session?"""
        json_dict = {
            "noDepart": True,
            "noReturn": True,
            "noTour": True,
            "departId": 0,
            "returnId": 0,
            "tourId": 0
        }

        resp = self.client.post('/itineraries/total', json=json_dict, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="text-center">Light speed to your favorite destinations across the galaxy!</h1>', html)
        self.assertIn('<div class="alert alert-danger text-center">You have to log in first, go to the &#39;Book A Trip&#39; page, and click &#39;Submit&#39; to access this route.</div>', html)

    def test_total_with_previous_total(self):
        """Does the view function correctly calculate total if the current itinerary already has a previous total?"""
        self.i.total = 500
        
        db.session.commit()

        json_dict = {
            "noDepart": '',
            "noReturn": '',
            "noTour": '',
            "departId": 5700,
            "returnId": 5701,
            "tourId": self.t2.id
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/total', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"total": "1,060"})

    def test_total_one_flight(self):
        """Does the view function correctly calculate total if current itinerary's total is 0 and we select 1 flight?"""
        json_dict = {
            "noDepart": '',
            "noReturn": True,
            "noTour": True,
            "departId": 5700,
            "returnId": 0,
            "tourId": 0
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/total', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"total": "250"})

    def test_total_two_flights(self):
        """Does the view function correctly calculate total if current itinerary's total is 0 and we select 2 flights?"""
        json_dict = {
            "noDepart": '',
            "noReturn": '',
            "noTour": True,
            "departId": 5700,
            "returnId": 5701,
            "tourId": 0
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/total', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"total": "500"})

    def test_total_two_flights_and_tour(self):
        """Does the view function correctly calculate total if current itinerary's total is 0 and we select 2 flights and a tour?"""
        json_dict = {
            "noDepart": '',
            "noReturn": '',
            "noTour": '',
            "departId": 5700,
            "returnId": 5701,
            "tourId": self.t2.id
        }

        with self.client.session_transaction() as session:
            session['curr_user'] = self.u.id
            session['itin'] = self.i.id

        resp = self.client.post('/itineraries/total', json=json_dict)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"total": "560"})