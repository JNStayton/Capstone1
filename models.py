from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database; call this function in app.py"""
    db.app = app
    db.init_app(app)


class Category(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
