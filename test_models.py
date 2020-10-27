import os
from unittest import TestCase
from models import *

os.environ['DATABASE_URL'] = "postgresql:///star-tours-test"

from app import app

db.create_all()

