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

class UserReviewsJourney(BaseTestCase):
    """
    Feature: An authenticated user should be able to write, edit, and delete their own reviews on games. User can view their review on a game's details page, view their reviews on their profile, and edit and delete their reviews from the profile or game's details page.
        Given I am an authenticated user
        When I click on a game's details page
        Then I should be able to post a review about that game
        And when I click the edit button for my review
        Then I can edit my existing review
        And when I navigate to my profile page
        Then I can click the link to view my review
        And then I can edit or delete the review from my reviews page
        And when I delete a review from my reviews page
        Then the review is deleted from the game's details page, my profile, and my reviews page"""
    def test_user_create_edit_delete_reviews(self):
        """User can create, edit, and delete reviews"""
        self.open(base_url)
        self.signup()
        self.login()

        #user navigates to game's details page
        self.click("a:contains('ROOT')")
        self.assert_title(' Root Page ')

        #user navigates to reviews section of game page
        self.click("a:contains('Reviews')")

        #user can view new review form
        self.assert_text("Leave Review for Root", "h4")

        #input review title and text
        self.type("#title", "Test")
        self.type("#text", "Test")
        self.click("#leave-review-btn")

        #review appears on page
        self.assert_text("div:contains('Test')")
        self.assert_element("#edit-review-Test-link")
        self.assert_element("#delete-review-Test-btn")

        #edit review
        self.click("#edit-review-Test-link")
        self.assert_title(" Edit Review ")
        self.click("#edit-review-btn")
        self.assert_element(".alert-success")
        self.assert_element("div:contains('Successfully edited your review!')")

        #review populates on my profile page
        self.assert_element("a:contains('Test')")

        #navigate to user's reviews page
        self.click("a:contains('See All Reviews')")

        #review appears on page
        self.assert_text("div:contains('Test')")
        self.assert_element("#edit-review-Test-link")
        self.assert_element("#delete-review-Test-btn")

        #delete review
        self.click("#delete-review-Test-btn")

        #redirected to home page with success 
        self.assert_title(" Home Page ")
        self.assert_element(".alert-success")
        self.assert_element("div:contains('Review deleted!')")

        #review is now gone from game details page
        self.click("a:contains('ROOT')")
        self.assert_element_absent("div:contains('Test')")

        #review is now gone from my profile page
        self.click("#my-profile-link")
        self.assert_element_absent("div:contains('Test')")

        #review is now gone from my reviews page
        self.click("a:contains('See All Reviews')")
        self.assert_element_absent("div:contains('Test')")

        self.delete_account()

