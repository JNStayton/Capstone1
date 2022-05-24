from flask import g, flash, redirect
from functools import wraps
import requests
from models import db, Category, Like, Review
from sqlalchemy import desc

base_url = 'https://api.boardgameatlas.com/api'
client_id = 'Vk9QEJ2umU'


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
    

def get_videos_for_game(game_id):
    """Search for most recent 6 videos on a game based on its game ID"""
    endpoint = f'/game/videos?limit=6&game_id={game_id}&client_id={client_id}'
    resp = requests.get(base_url + endpoint)
    json = resp.json()
    videos = json['videos']
    return videos


def fix_video_embed_link(videos):
    """Receive videos; change URL format to embeded link format to display in HTML; return iterable list of videos"""
    videos_list = []
    for video in videos:
        link = video['url']
        title = video['title']
        base_url='https://www.youtube.com/embed/'
        id = link[link.find("=")+1::]
        new_url = base_url+id
        videos_list.append((title, new_url))
    return videos_list


def get_images_for_game(game_id):
    """Retrieve alternate images for game based on game_id"""
    endpoint = f'/game/images?limit=10&id={game_id}&client_id={client_id}'
    resp = main_request(base_url, endpoint)
    json = resp.json()
    images = json['images']
    return images


def main_request(base_url, endpoint):
    """Receives a base url and the endpoint for that url, 
    returns the parsed JSON response"""
    resp = requests.get(base_url + endpoint)
    json = resp.json()
    games = json['games']
    return games


def get_likes(user):
    """Retrieve liked game ids for a user"""
    if user:
        likes = user.liked_games
        return [game.game_id for game in likes]
    else:
        return []


def add_or_remove_like(game_id, game_ids_list, user):
    """Function for adding or removing a liked game from db"""
    if game_id in game_ids_list:
        Like.query.filter_by(game_id=game_id, user_username=user.username).delete()
    else:
        liked_game = Like(user_username=g.user.username, game_id=game_id)
        db.session.add(liked_game)


def get_reviews_by_game(game_id):
    """Returns all reviews made for a game by game ID"""
    reviews = Review.query.filter_by(game_id=game_id).all()
    return reviews


def get_reviews_by_user(username):
    """Returns all reviews made by a user"""
    reviews = Review.query.filter_by(user_username=username).all()
    return reviews


def get_latest_reviews_by_user(username):
    """Returns most recent 10 reviews made by a user"""
    reviews = Review.query.filter_by(user_username=username).order_by(desc(Review.timestamp)).limit(10).all()
    return reviews

def authorized(f):
    """Decorator function for checking user authorization"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function