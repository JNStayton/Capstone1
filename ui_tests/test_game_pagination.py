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

class GamePaginationJourney(BaseTestCase):
    """
    Feature: Basic pagination is functional; 
    Next and Back buttons appear on bottom of page when there are more than 10 games in a search
    Scenario: For Top Rated games, I can click to view paginated results of games. I can go back to previous results, or forward to later results. I cannot go back when on the first page, and I cannot search beyond the maximum search results.
        Given I am searching for games sorted by <type or category>
        When I scroll to the bottom of the page
        Then I see the 'next' button
        And when I click the 'next' button
        Then I am taken to the next 10 search results for <type or category>
        And when I click the 'back' button
        Then I am taken back to the prior 10 search results
        And when I try to view beyond the search count by altering the url
        Then I am taken to an error page with a link to redirect home
    """

    def test_user_can_view_and_click_pagination_btns(self):
        """
        Given I am searching for games sorted by <type or category>
        When I scroll to the bottom of the page
        Then I see the 'next' button
        And when I click the 'next' button
        Then I am taken to the next 10 search results for <type or category>
        """ 
        self.signup()
        self.login()
        #we can see the number 1 game, but not the number 11 game 
        self.assert_element('a:contains("ROOT")')
        #we see that we are being shown results 1-10 of page 1
        self.assert_element('p:contains("Showing results 1 - 10")')
        self.assert_element_absent('a:contains("THE CASTLES OF BURGUNDY")')
        #we scroll to the bottom of the page
        self.scroll_to_bottom()

        #we see the next button, but not the back button, and click next
        self.assert_element("#next-btn")
        self.assert_element_absent("#back-btn")
        self.click("#next-btn")

        #we are not on page two of search results
        page_2 = self.get_current_url()
        self.assert_equal(page_2, base_url+"games/2/Rated")
        #we see game number 11, but not game number 1
        self.assert_element('a:contains("THE CASTLES OF BURGUNDY")')
        #we see that we are being shown results 11-20 of page 2
        self.assert_element('p:contains("Showing results 11 - 20")')
        self.assert_element_absent('a:contains("ROOT")')

        #we scroll to the bottom again and see next and back buttons
        self.scroll_to_bottom()
        self.assert_element("#next-btn")
        self.assert_element("#back-btn")

        #user can now click back to view prior results
        self.click("#back-btn")

        #we can see the number 1 game, but not the number 11 game 
        self.assert_element('a:contains("ROOT")')
        #we see that we are being shown results 1-10 of page 1
        self.assert_element('p:contains("Showing results 1 - 10")')
        self.assert_element_absent('a:contains("THE CASTLES OF BURGUNDY")')
        #we scroll to the bottom of the page
        self.scroll_to_bottom()

        #we see the next button, but not the back button, and click next
        self.assert_element("#next-btn")
        self.assert_element_absent("#back-btn")
        self.delete_account()


    def test_user_can_update_url_to_view_pagination_results(self):
        """
        Given I am searching for games by <type or category>
        When I update the url to a page count in bounds
        Then I am taken to that page displaying those results
        And when I try to view beyond the search count by altering the url
        Then I am taken to an error page with a link to redirect home
        """
        self.signup()
        self.login()
        #we click the animals badge link on the number one game displayed and are redirected to the top animal games search page
        self.open(base_url+"games/1/Animals")
        self.assert_element('h2:contains("Top Animals Games")')
        animals_page_1 = self.get_current_url()
        self.assert_equal(animals_page_1, base_url+"games/1/Animals")
        self.assert_element('p:contains("Showing results 1 - 10")')

        #we can update the URL to jump to a page in results
        self.open(base_url+"games/10/Animals")
        self.assert_element('p:contains("Showing results 91 - 100")')

        #but if we go out of bounds we are taken to an error page
        self.open(base_url+"games/999/Animals")
        self.assert_element('h1:contains("Uh oh")')
        error_page = self.get_current_url()
        self.assert_equal(error_page, base_url+"error")

        #link in error message redirects us to the home page
        self.click('a:contains("here")')
        home_page = self.get_current_url()
        self.assert_equal(home_page, base_url+"games/1/Rated")
        self.delete_account()
        






