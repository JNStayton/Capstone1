import os

from flask import Flask, render_template, redirect, request, g, session, flash

from models import db, connect_db, Category, User, Review
from forms import NewUser, LoginForm, ReviewForm, EditUserForm

from helpers import get_game_categories, get_category_names, get_videos_for_game, fix_video_embed_link, main_request, get_likes, add_or_remove_like, get_reviews_by_game, get_reviews_by_user, get_latest_reviews_by_user, authorized


CURR_USER = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    os.environ.get('DATABASE_URL', 'postgresql:///boardgames'))

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', "keep it secret, keep it safe")

connect_db(app)
db.create_all()

#if the categories table is empty, run get_game_categories to fetch the API categories data
if db.session.query(Category).first() == None:
    get_game_categories()


base_url = 'https://api.boardgameatlas.com/api'
client_id = 'Vk9QEJ2umU'

############################################################################################
# SEARCH ROUTES for API
############################################################################################

@app.route('/games/top_games')
def show_top_games():
    """Get game data from BGA based on its rank and display in groups of 24"""

    games = main_request(base_url, f'/search/?order_by=rank&limit=24&client_id={client_id}')
    
    category_dict = get_category_names(games)

    game_ids_list = get_likes(g.user)

    return render_template('search_results.html', games=games, category_dict=category_dict, game_ids_list=game_ids_list, type='Rated')


@app.route('/games/<category_name>')
def show_games_in_category(category_name):
    """Show top 24 games in a specific category"""

    category = Category.query.filter_by(name=category_name).first()
    
    games = main_request(base_url, f'/search/?categories={category.id}&limit=24&order_by=rank&client_id={client_id}')

    category_dict = get_category_names(games)
    game_ids_list = get_likes(g.user)

    return render_template('search_results.html', games=games, game_ids_list=game_ids_list, category_dict=category_dict, type=category_name)


@app.route('/games/player_count_<int:num>')
def show_games_by_player_count(num):
    """Show top ranked games based on minimum number of players"""

    games = main_request(base_url, f'/search/?min_players={num}&order_by=rank&limit=24&client_id={client_id}')

    category_dict = get_category_names(games)
    game_ids_list = get_likes(g.user)

    return render_template('search_results.html', games=games, game_ids_list=game_ids_list, category_dict=category_dict, type=f'{num}+ Players')


@app.route('/games/player_min_<int:min_num>&player_max_<int:max_num>')
def show_games_by_player_range(min_num, max_num):
    """Show top ranked games based on min and max player range"""

    games = main_request(base_url, f'/search/?min_players={min_num}&max_players={max_num}&limit=24&order_by=rank&client_id={client_id}')

    category_dict = get_category_names(games)
    game_ids_list = get_likes(g.user)

    return render_template('search_results.html', games=games, game_ids_list=game_ids_list, category_dict=category_dict, type=f'{min_num}-{max_num} Players')


@app.route('/games/name')
def search_games_by_name():
    """Search the API by game name, return first 24 to match the name OR, if search form is empty, return top 24 games"""
    query = request.args.get('query')

    if query == '':
        games = main_request(base_url, f'/search?limit=24&client_id={client_id}')
    else:
        games = main_request(base_url, f'/search/?name={query}&fuzzy_match=true&limit=24&client_id={client_id}')
    
    category_dict = get_category_names(games)
    game_ids_list = get_likes(g.user)

    return render_template('search_results.html', games=games, game_ids_list=game_ids_list, category_dict=category_dict, type=f'{query.capitalize()}')


############################################################################################
# DISPLAY ROUTES
############################################################################################

@app.route('/games/game/<game_id>', methods=['GET', 'POST'])
def show_game_page(game_id):
    """Show info page for individual game;
    If registered, show form to leave review for game and handle form submit"""

    form=ReviewForm()

    games = main_request(base_url, f'/search/?ids={game_id}&client_id={client_id}')
    
    category_dict = get_category_names(games)
    game = games[0]

    videos = fix_video_embed_link(get_videos_for_game(game_id))

    game_ids_list = get_likes(g.user)

    reviews = get_reviews_by_game(game_id)

    if g.user:
        if form.validate_on_submit():
            review = Review(title = form.title.data,
                            text = form.text.data,
                            game_id=game_id,
                            user_username = g.user.username)
            g.user.game_reviews.append(review)
            db.session.commit()
            return redirect(f'/games/game/{game_id}#reviews')

    return render_template('game_page.html', game=game, category_dict=category_dict, form=form, videos=videos, game_ids_list=game_ids_list, reviews=reviews)


@app.route('/users/profile/<username>')
def show_user_page(username):
    """Show a user's profile page"""
    user = User.query.get_or_404(username)

    liked_list = get_likes(user)

    game_ids = ','.join([str(id) for id in liked_list])

    if game_ids:
        games = main_request(base_url, f'/search/?ids={game_ids}&client_id={client_id}')
    else:
        games = {}

    game_ids_list = get_likes(g.user)

    reviews = get_latest_reviews_by_user(username)

    return render_template('show_user.html', user=user, games=games, game_ids_list=game_ids_list, reviews=reviews)


@app.route('/users/<username>/reviews')
def show_user_reviews(username):
    """Show all reviews left by a single user"""
    user = User.query.get_or_404(username)
    reviews = get_reviews_by_user(user.username)

    game_ids_list = []
    for review in reviews:
        game_ids_list.append(review.game_id)
    
    game_ids = ','.join([str(id) for id in game_ids_list])
    games = main_request(base_url, f'/search/?ids={game_ids}&client_id={client_id}')

    game_names = []
    for game in games:
        game_names.append(game['name'])

    game_dict = {game_ids_list[i]: game_names[i] for i in range(len(game_ids_list))}

    return render_template('all_reviews.html', reviews=reviews, game_dict=game_dict, user=user)


############################################################################################
# LOGIN / LOGOUT and AUTHENTICATION ROUTES
############################################################################################

@app.before_request
def add_user_to_g():
    """If the user is logged in, add them to g"""

    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])
    else:
        g.user = None


@app.route('/')
def home():
    """If not logged in, render login page;
    if logged in, redirect to /top_games"""
    if not g.user:
        return redirect('/login')
    return redirect('/games/top_games')


@app.route('/register', methods=['GET', 'POST'])
def signup():
    """Handle user registration; create user and add to DB, then redirect to home page"""
    if g.user:
        flash('You already have an account with us.', 'warning')
        return redirect('/')

    form = NewUser()

    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
            )
        db.session.commit()
        # add new user to g, and set session
        session[CURR_USER] = user.username
        flash(f'Successfully created account! Welcome, {user.username}!', 'success')
        return redirect('/games/top_games')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login a registered user"""
    if g.user:
        flash(f"You're already logged in, {g.user.username.capitalize()}!", 'warning')
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            session[CURR_USER] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect('/games/top_games')
        
        flash('Oops! Invalid username or password. Please try again or create an account!', 'danger')

    return render_template('login_user.html', form=form)



@app.route('/logout')
def logout_user():
    """Logout a registered user"""
    if CURR_USER in session:
        del session[CURR_USER]
        flash('See you next time!', 'success')
    return redirect('/games/top_games')



@app.route('/users/edit', methods=['GET', 'POST'])
@authorized
def edit_user_profile():
    """Edit a user's account"""
    
    user = User.query.get_or_404(g.user.username)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data

        db.session.add(user)
        db.session.commit()
        flash(f'Successfully updated username to {user.username}!', 'success')
        return redirect(f'/users/profile/{g.user.username}')
    
    else:
        return render_template('edit_user.html', form=form)


@app.route('/users/delete', methods=['POST'])
@authorized
def delete_user_account():
    """Delete user account"""

    db.session.delete(g.user)
    del session[CURR_USER]
    db.session.commit()

    flash(f"Account deleted. We're sad to see you go!", 'danger')
    return redirect('/')


@app.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@authorized
def edit_review(review_id):
    """Edit review if authorized user"""

    review = Review.query.get_or_404(review_id)

    form = ReviewForm(obj=review)

    if review.user_username != g.user.username:
        flash('Unauthorized; that is not your review to edit.', 'danger')
        return redirect(f'/users/profile/{g.user.username}')

    if form.validate_on_submit():
        review.title = form.title.data,
        review.text = form.text.data
        db.session.commit()
        flash('Successfully edited your review!', 'success')
        return redirect(f'/users/profile/{review.user_username}')
    
    return render_template('edit_review.html', form=form, review=review)



@app.route('/reviews/<int:review_id>/delete', methods=['POST'])
@authorized
def delete_review(review_id):
    """Delete review if authorized user"""

    review = Review.query.get_or_404(review_id)

    if review.user_username != g.user.username:
        flash('Unauthorized; that is not your review to delete.', 'danger')
        return redirect(f'/users/profile/{g.user.username}')

    db.session.delete(review)
    db.session.commit()
    flash('Review deleted!', 'success')
    return redirect('/')


@app.route('/users/like_game/<game_id>', methods=["POST"])
@authorized
def like_game(game_id):
    """Logged in user may like or unlike a game"""
    
    games = main_request(base_url, f'/search/?ids={game_id}&client_id={client_id}')
    game_id = games[0]['id']

    game_ids_list = get_likes(g.user)

    add_or_remove_like(game_id, game_ids_list, g.user)

    db.session.commit()

    return redirect(request.referrer)