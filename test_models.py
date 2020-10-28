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