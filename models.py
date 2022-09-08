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



class Like(db.Model):
    """Mapping user likes to API game IDs"""

    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)

    user_username = db.Column(db.String, db.ForeignKey('users.username', ondelete='CASCADE', onupdate='CASCADE'))

    game_id = db.Column(db.String, nullable=False)


class Review(db.Model):
    """A review of a game"""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True,)

    title = db.Column(db.String(75), nullable=False)

    text = db.Column(db.String(500), nullable=False,)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    game_id = db.Column(db.String, nullable=False)

    user_username = db.Column(db.String, db.ForeignKey('users.username', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


class User(db.Model):
    """Users in the db"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key = True, nullable=False)

    email = db.Column(db.String, unique=True, nullable=False)

    password = db.Column(db.Text, nullable=False)

    liked_games = db.relationship('Like', backref='user')

    game_reviews = db.relationship("Review", cascade='all, delete')

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