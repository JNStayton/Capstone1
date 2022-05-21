import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, User, Review, Like

os.environ['DATABASE_URL'] = "postgresql:///boardgames_test"

from app import app, CURR_USER

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class SearchViewFunctionsTestCase(TestCase):
    """Test the search view functions that handle the API calls and return templates displaying the data from the search parameters"""

    def test_show_top_games(self):
        """Tests the call for top 24 ranked games"""

        with app.test_client() as c:
            resp = c.get('/games/top_games')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Top Rated Games', str(resp.data))
            self.assertIn('PRICE', str(resp.data))
            self.assertIn('CATEGORIES', str(resp.data))
            self.assertIn('INFO', str(resp.data))

    def test_show_games_in_category(self):
        """Test the call for top 24 games within a certain category"""

        with app.test_client() as c:
            resp = c.get('/games/Animals')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Top Animals Games', str(resp.data))

    def test_show_games_by_player_count(self):
        """Test the call for top 24 games that are X or more players"""

        with app.test_client() as c:
            resp = c.get('/games/player_count_2')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Top 2+ Players Games', str(resp.data))

    def test_show_games_by_player_range(self):
        """Test the call for top 24 games that are between X and Y number of players"""
        
        with app.test_client() as c:
            resp = c.get('/games/player_min_2&player_max_4')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Top 2-4 Players Games', str(resp.data))

    def test_search_games_by_name(self):
        """Test the call for top 24 games that match a fuzzy search on the typed name input"""

        with app.test_client() as c:
            resp = c.get('/games/name?query=scythe')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('scythe', str(resp.data))


class DisplayViewFunctionsTestModel(TestCase):
    """Tests the view functions that handle showing pages """

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Review.query.delete()

        self.client = app.test_client()

        #create test users
        self.test_user = User.register(username='test1',
                                    email='test@test.com',
                                    password='test')

        db.session.commit()

        # add test review for test_user1; have test_user2 like the test message
        review = Review(user_username='test1', title='testreview', text='testtesttest', game_id='yqR4PtpO8X')
        db.session.add(review)
        db.session.commit()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_show_game_page(self):
        """Test the route displays information for a game, including reviews for that game;
        Tests that the page renders a review form if the user is logged in"""

        #test that when logged in, both reviews and review form are displayed
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = self.test_user.username
            
            resp=c.get('/games/game/yqR4PtpO8X')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Scythe', str(resp.data))
            self.assertIn('testtesttest', str(resp.data))
            self.assertIn('Leave Review for Scythe', str(resp.data))

        #test that when not logged in, reviews are displayed, but not review form
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = ''
            
            resp=c.get('/games/game/yqR4PtpO8X')
            self.assertIn('testtesttest', str(resp.data))
            self.assertNotIn('Leave Review for Scythe', str(resp.data))

    def test_show_user_page(self):
        """Test the route displays information about a user and, if user is logged in, that the update account info form displays"""

        with self.client as c:
            resp=c.get('/users/profile/test1')
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test1\\\'s Profile", str(resp.data))
            self.assertIn('testreview', str(resp.data))
            self.assertNotIn("Edit Account", str(resp.data))

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = self.test_user.username
            
            resp=c.get('/users/profile/test1')
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Account", str(resp.data))
            self.assertIn('testreview', str(resp.data))

    def test_show_user_reviews(self):
        """Tests the route displays all reviews by a given user, including which game the reviews are for"""

        with self.client as c:
            resp=c.get('/users/test1/reviews')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test1', str(resp.data))
            self.assertIn('testreview', str(resp.data))
            self.assertIn('testtesttest', str(resp.data))
            self.assertIn('Scythe', str(resp.data))
            
    
class UserLoginAndAuthenticationViewFunctionsTestModel(TestCase):
    """Tests the view function routes for user authenticaion and functionality"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Review.query.delete()

        self.client = app.test_client()

        #create test users
        self.test_user = User.register(username='test1',
                                    email='test@test.com',
                                    password='test')

        db.session.commit()

        # add test review for test_user1; have test_user2 like the test message
        review = Review(user_username='test1', title='testreview', text='testtesttest', game_id='yqR4PtpO8X')
        db.session.add(review)
        db.session.commit()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_home(self):
        """Tests that user is redirected to appropriate page based on login status"""

        #If user logged in, redirect to 'home', ie top rated games page
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = self.test_user.username

            resp=c.get('/', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Top Rated Games', str(resp.data))

        #if user not logged in, redirect to login page
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = ''

            resp=c.get('/', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', str(resp.data))

    def test_signup(self):
        """Test that a logged in user is redirected and shown a message if trying to register a new account"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = self.test_user.username

            resp=c.get('/register', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('You already have an account with us.', str(resp.data))
            self.assertIn('Top Rated Games', str(resp.data))

    def test_login(self):
        """Test that route displays login form"""

        with self.client as c:
            resp=c.get('/login')
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Login', str(resp.data))

    def test_logout(self):
        """Test that route logs out a logged-in user and displays message"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER] = self.test_user.username

            resp=c.get('logout', follow_redirects=True)
            self.assertIn('See you next time', str(resp.data))

