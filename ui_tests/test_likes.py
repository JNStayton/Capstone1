from seleniumbase import BaseCase

base_url = 'https://duncans-toy-chest.herokuapp.com/'

class BaseTestCase(BaseCase):
    """login and logout methods allow for reduced redundancy with testing journeys"""
    username = "test"
    password="password123"
    email="test@test.com"

    def setUp(self):
        super(BaseTestCase, self).setUp()

    def tearDown(self):
        self.save_teardown_screenshot()  # If test fails, or if "--screenshot"
        super(BaseTestCase, self).tearDown()

    def signup(self):
        """Signs up a unique test user"""
        username = "test"
        password="password123"
        email="test@test.com"

        self.open(base_url)
        self.click('a:contains("Sign up")')
        self.type("#username", username)
        self.type("#password", password)
        self.type("#email", email)

        self.click("#register-btn")
        self.click("#logout")


    def login(self):
        """Logs in with sample user named after my cat, Jareth"""
        self.open(base_url)
        self.type("#username", "test")
        self.type("#password", "password123")
        self.click("#login-btn")

    def logout(self):
        """Logs out of sample user"""
        self.click("#logout")
    
    def delete_account(self):
        self.click("#my-profile-link")
        self.click("#delete-user-btn")

class LikesAndReviewsJourney(BaseTestCase):
    """
    Feature: Authenticated user can like, unlike, and leave reviews on games. User can edit their own reviews.
    Scenario: On the home page, user clicks the heart button on a game and it changes to red, and adds the game to their "favorites". User can view all their favorite games on their profile. User can click the heart button again to unlike a game, and see it removed from their favorites. User can leave reviews on games, view and edit the reviews they have left.
    """
    def test_authenticated_user_likes_game(self):
        """User can click the heart button to add a game to their favorites"""

        self.login()

        #clicking like button for game updates its class to have a red background
        self.click("#Root-like-btn")
        # self.assert_element(".btn-danger")

        #when we navigate to our profile, we can view the liked game
        self.click("#my-profile-link")
        self.assert_element("h5:contains('Root')")
        
