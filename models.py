from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database; call this function in app.py"""
    db.app = app
    db.init_app(app)


class Category(db.Model):
    """Game categories from API"""

    __tablename__ = 'categories'

    id = db.Column(
        db.String, 
        primary_key = True)
    name = db.Column(db.String)


class Likes(db.Model):
    """Mapping user likes to API game IDs"""

    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    game_id = db.Column(db.String, nullable=False)


class Review(db.Model):
    """A review of a game"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True,)

    text = db.Column(db.String(500), nullable=False,)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User')


class User(db.Model):
    """Users in the db"""

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    email = db.Column(db.String, unique=True, nullable=False)

    username = db.Column(db.String(20), unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    liked_games = db.relationship("Likes")

    game_reviews = db.relationship("Review")

    @classmethod
    def register(cls, username, email, password):
        """Registers a user; hashes password and adds user to db."""

        hashed = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        Return user whose password hash matches this password.
        If user doesn't exist, or passwords don't match, returns False.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False