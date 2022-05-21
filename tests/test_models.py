import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Review, Like

os.environ['DATABASE_URL'] = "postgresql:///boardgames-test"

from app import app

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Review.query.delete()

        # add test user to test db
        test1 = User.register(username= 'test1', password='test1', email='test1@test.com')

        db.session.commit()

        self.test1 = test1

    def tearDown(self):
        """Tear down test client to start clean after each test"""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does model work?"""

        u = User(
            email='test@test.com',
            username='testuser',
            password='password'
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.game_reviews), 0)
        self.assertEqual(len(u.liked_games), 0)

    def test_user_registration(self):
        """Does user registration work?"""

        user = User.register(
            email='test@test.com',
            username='testuser',
            password='password'
        )

        db.session.commit()

        user1 = User.query.get('testuser')

        self.assertEqual(user, user1)

    def test_user_authentication(self):
        """Test username and password authentication"""

        test1 = User.authenticate('test1', 'test1')
        # test valid authentication
        self.assertEqual(self.test1.authenticate('test1', 'test1'), test1)

        # test invalid username
        self.assertEqual(self.test1.authenticate('wasedfj', 'test1'), False)

        #test invalid password
        self.assertEqual(self.test1.authenticate('test1', 'quwaygeuh'), False)


class LikeTestCase(TestCase):
    """Test model for likes"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Review.query.delete()

        # add test user to test db
        test1 = User.register(username= 'test1', password='test1', email='test1@test.com')

        db.session.commit()

        self.test1 = test1

        self.game_id = 'test123'

    def tearDown(self):
        """Tear down test client to start clean after each test"""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_like_model(self):
        like = Like(user_username=self.test1.username, game_id=self.game_id)
        db.session.add(like)
        db.session.commit()

        self.assertIn(like, self.test1.liked_games)


class ReviewModelTest(TestCase):
    """Test model for Reviews"""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Review.query.delete()

        # add test user to test db
        test1 = User.register(username= 'test1', password='test1', email='test1@test.com')

        db.session.commit()

        self.test1 = test1

        self.game_id = 'test123'

    def tearDown(self):
        """Tear down test client to start clean after each test"""
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_review_model(self):
        """Test creation of user and relationship to user"""
        review = Review(title='test', text='test', game_id=self.game_id, user_username=self.test1.username)
        db.session.add(review)
        db.session.commit()

        self.assertIn(review, self.test1.game_reviews)
