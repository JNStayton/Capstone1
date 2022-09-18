from seleniumbase import BaseCase

base_url = 'https://duncans-toy-chest.herokuapp.com/'
fake_user = 'blarggglhlhlh58920496!!%C'
fake_password = 'thisisaverybadpassword123456'

class HomePageUserJourney(BaseCase):
    """
    Feature: Basic user navigation works: login, view profile, log out
    Scenario: User logs in to site
        Given I am an existing user
        When I navigate to the base url
        Then I should be redirected to the login page
        When I enter my credentials
        Then I should be redirected to the home page
        When I click on 'My Profile' link in the navbar
        Then I should be redirected to my profile
        When I click on 'Logout' in the navbar
        Then I should be logged out
        And I should be redirected to the home page"""

    def test_home_page_redirects_when_not_logged_in(self):
        """
        Given I open the home page url
        when I am not currently logged in
        Then I am redirected to the login page
        """

        #open home page
        self.open(base_url)
        redirect_to_login_url = self.get_current_url()
        #redirected to login page
        self.assert_equal(redirect_to_login_url, base_url+"login")
        self.assert_text("Login", "h3")
        #page title for login page
        self.assert_title(" Login Page ")

    def test_user_can_login_and_logout(self):
        """
        Given I have been redirected to the login page
        When I enter my credentials in the login form
        Then I am redirected to the home page
        And when I click 'My Profile' in the navbar
        Then I can view my profile
        And when I click 'Logout' in the navbar
        Then I am successfully logged out of the website
        """

        self.open(base_url)

        #navbar appears on page
        self.assert_element(".navbar")

        #Login header appears on page
        self.assert_exact_text("Login", "h3")

        #link to sign up appears on page
        self.assert_element('a:contains("Sign up!")')

        #username input appears on page
        self.assert_element("#username")
        self.type("#username", "Jareth")

        #password input appears on page
        self.assert_element("#password")
        self.type("#password", "jarethcat")

        #button to log in appears on page
        self.assert_element("#login-btn")
        self.click("#login-btn")

        #successful login alert shows
        self.assert_element(".alert-success")

        #page redirected to Home (/games/1/Rated)
        home_page_url = self.get_current_url()
        self.assert_equal(home_page_url, base_url+"games/1/Rated")
        self.assert_title(" Home Page ")
        self.assert_text("Top Rated Games", "h2")

        #dismiss successful login alert
        self.click(".close")
        self.assert_element_absent(".alert-success")

        #user can view and click on "my profile" and "logout" links in navbar
        self.assert_element("#my-profile-link")
        self.assert_element("#logout")

        #user clicks on "my profile" and is redirected to my profile page
        self.click("#my-profile-link")
        self.assert_title(" Jareth Page ")

        #user can log out
        self.click("#logout")
        self.assert_element(".alert-success")

    def test_error_alerts_on_incorrect_username_on_login(self):
        """Given I am on the home page
        And attempting to log in
        When I enter an incorrect or unregistered username
        Then I see an alert with an invalid credentials error message
        And the error alert is dismissible"""

        self.open(base_url)

        #invalid password input
        self.assert_element("#username")
        self.type("#username", fake_user)

        #password input
        self.assert_element("#password")
        self.type("#password", "jarethcat")

        self.click("#login-btn")

        #error login alert shows
        self.assert_element(".alert-danger")
        self.assert_element('div:contains("Oops! Invalid username or password. Please try again or create an account!")')

        #alert is dismissible 
        self.click(".close")   
        self.assert_element_absent(".alert-danger")

    def test_error_alerts_on_incorrect_password_on_login(self):
        """Given I am on the home page
        And attempting to log in
        When I enter my username with the incorrect password
        Then I see an alert with an invalid credentials error message
        And the error alert is dismissible"""

        self.open(base_url)

        #invalid password input
        self.assert_element("#username")
        self.type("#username", "Jareth")

        #password input
        self.assert_element("#password")
        self.type("#password", fake_password)

        self.click("#login-btn")

        #error login alert shows
        self.assert_element(".alert-danger")
        self.assert_element('div:contains("Oops! Invalid username or password. Please try again or create an account!")')

        #alert is dismissible 
        self.click(".close")   
        self.assert_element_absent(".alert-danger")

    def test_error_alerts_on_registering_with_taken_username_or_password(self):
        """Given I am on the home page
        And I attempt to sign up as a user
        When I enter a username or email that has already been registered
        Then I cannot register with that email or password
        And I see an alert with a "username or email already registered" message
        And the error alert is dismissible"""

        self.open(base_url)

        #link to sign up appears on page
        self.assert_element('a:contains("Sign up!")')
        self.click("signup-redirect-link")

        #redirected to register page
        self.assert_title(" Register ")

        #taken username input
        self.assert_element("#username")
        self.type("#username", "Jareth")

        # #password input
        self.assert_element("#password")
        self.type("#password", "password")

        self.click("#register-btn")

        # #error login alert shows
        self.assert_element(".alert-warning")
        self.assert_element('div:contains("That username or email is already registered with us!")')

        # #alert is dismissible 
        self.click(".close")   
        self.assert_element_absent(".alert-warning")



