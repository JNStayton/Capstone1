from seleniumbase import BaseCase

base_url = 'https://duncans-toy-chest.herokuapp.com/login'

class HomeTest(BaseCase):
    """
    Tests the user login journey;
    Scenario: User logs in to site"""
    def test_home_page(self):
        #open home page
        self.open(base_url)
        #page title for login page
        self.assert_title(" Login Page ")
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
        self.assert_title(" Home Page ")
        #dismiss successful login alert
        self.click(".close")
        self.assert_element_absent(".alert-success")
        #user can view and click on "my profile" link in navbar
        self.assert_element()