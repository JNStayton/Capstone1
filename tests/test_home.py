from seleniumbase import BaseCase
#BaseCase is a test class in Selenium that we can use for basic UI testing
#Check out documentation at seleniumbase.io

#####################################################
# This test file is to test our home page; `duncans-toy-chest.herokuapp.com/` which should:
# 1. If user not logged in, redirects to login page
# 2. If user is logged in, redirects to FIRST PAGE of top rated games
#####################################################

base_url = 'https://duncans-toy-chest.herokuapp.com/'

class HomePageTest(BaseCase):
    def test_home_page_renders(self):
        # open home page
        self.open(base_url)

        # assert page title; we are not logged in, so it should redirect us to the login page
        self.assert_title("Login Page")

        # type username in form input
        self.type('#username', 'jareth')

        #type password in form input
        self.type('#password', 'jarethcat')