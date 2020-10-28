import os
from unittest import TestCase
from models import *

os.environ['DATABASE_URL'] = "postgresql:///star-tours-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test user model"""
    
    def setUp(self):
        """Add sample user"""
        # We have to delete itineraries from any previous tests first, otherwise we'll get an error saying that the user's table 
        # is still referencing the itinerary's id
        Itinerary.query.delete()
        User.query.delete()

        self.u = User.signup('test@test.com', 'testy1', 'testing!', 'Testy', 'McTestface')

        db.session.add(self.u)
        db.session.commit()

    def tearDown(self):
        """Remove any fouled transactions"""
        db.session.rollback()

    def test_signup_success(self):
        """Can you sign up a new user successfully?"""
        u2 = User.signup('test2@test.com', 'testy2', 'testing2!', 'Obi-Wan', 'Kenobi')
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u2.id, u2.id)
        self.assertEqual(u2.email, 'test2@test.com')
        self.assertEqual(u2.username, 'testy2')

    def test_signup_fail(self):
        """Does User.signup return an array of strings when email and username are not unique?"""
        u2 = User.signup('test@test.com', 'testy1', 'testing!', 'Testy', 'McTestface')

        self.assertEqual(u2, ["That username has already been taken.  Please choose another one.", "That email already has an account with us.  Please use another."])

    def test_authenticate_success(self):
        """Can we successfully authenticate a user?"""
        test = User.authenticate('testy1', 'testing!')

        self.assertEqual(test, self.u)

    def test_authenticate_fail(self):
        """Do we get False when we enter the wrong username/password?"""
        test = User.authenticate('JabbaNoBotha', 'daeWannaWanga')

        self.assertEqual(test, False)

    def test_verify_success(self):
        """Do we get the user when verify is successful?"""
        test = User.verify('test@test.com', 'testy1', 'testing!')

        self.assertEqual(test, self.u)

    def test_verify_fail(self):
        """Do we get False when verify fails?"""
        test = User.verify('jabba2@jabba.com', 'JabbaNoBotha', 'daeWannaWanga')

        self.assertEqual(test, False)

    def test_update_password(self):
        """Does this update user's password?"""
        self.u.update_password('daeWannaWanga')
        db.session.commit()

        test = User.authenticate('testy1', 'daeWannaWanga')

        self.assertEqual(test, self.u)

class ItineraryModelTestCase(TestCase):
    """Test Itinerary model"""
    
    def setUp(self):
        """Add sample user and itinerary"""
        # We have to delete itineraries first, otherwise we'll get an error saying that the user's table is still referencing
        # the itinerary's id
        Itinerary.query.delete()
        User.query.delete()

        self.u = User.signup('test@test.com', 'testy1', 'testing!', 'Testy', 'McTestface')
        db.session.add(self.u)
        db.session.commit()

        self.itin = Itinerary(user_id=self.u.id)
        db.session.add(self.itin)
        db.session.commit()

    def tearDown(self):
        """Remove any fouled transactions"""
        db.session.rollback()

    def test_user_itin_relationship(self):
        """Make sure that the itinerary is connected to the user"""
        self.assertEqual(len(self.u.itineraries), 1)
        self.assertEqual(self.u.itineraries[0].id, self.itin.id)

    def test_add_commas_to_total(self):
        """Make sure the add_commas_to_total method works as intended"""
        self.itin.total = 1560
        db.session.commit()

        self.assertEqual(self.itin.add_commas_to_total(), '1,560')