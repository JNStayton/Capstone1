from flask import Flask, render_template, redirect, session, flash, jsonify
import requests
from models import db, connect_db, Category

app = Flask(__name__)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///boardgames"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "keep it secret, keep it safe"

connect_db(app)
db.create_all()

base_url = 'https://api.boardgameatlas.com/api'
client_id = 'Vk9QEJ2umU'

############################################################################################
# HELPER FUNCTIONS TO PULL LATER 
############################################################################################

def get_game_categories():
    """Get game category information and save to database table Category"""
    categories_resp = requests.get(f'{base_url}/game/categories?client_id={client_id}')
    json = categories_resp.json()
    categories = json['categories']

    for category in categories:
        category = Category(id = category['id'], name = category['name'])
        db.session.add(category)
    
    db.session.commit()

def get_category_names(games):
    """Accepts games JSON;
    Saves the category ids attributed to the game to a list;
    Queries the DB to get the names for categories by ID;
    returns a dictionary with the game's name as a key, and a list of category names as the value"""
    category_dict = {}
    for game in games:
        catlist = [category['id'] for category in game['categories'] if game['categories']]
        q = db.session.query(Category.name).filter(Category.id.in_(catlist)).all()
        category_names = [category[0] for category in q]
        category_dict[f"{game['name']}"] = category_names
    
    return category_dict
    

############################################################################################
# ROUTES
############################################################################################

@app.route('/')
def show_homepage():
    """Get game data from BGA based on its rank and display in groups of 12"""

    resp = requests.get(f'{base_url}/search/?order_by=rank&limit=12&&client_id={client_id}')

    json = resp.json()
    games = json['games']

    category_dict = get_category_names(games)

    return render_template('home.html', games=games, category_dict=category_dict)
