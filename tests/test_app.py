import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, User, Review, Like

os.environ['DATABASE_URL'] = "postgresql:///boardgames-test"

from app import app, CURR_USER

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


