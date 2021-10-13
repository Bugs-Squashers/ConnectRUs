import unittest
import requests


class TestMain(unittest.TestCase):
    URL = 'http://192.168.0.32:5000/'

    # Amanda's Test
    def test_home(self):
        r = requests.get(self.URL)
        # status code 200 means we got a response back
        self.assertEquals(r.status_code, 200)
        # since no user is logged in, the response should be "Hello World!"
        self.assertEquals(r.text, "Hello World!")

    # Sandra's Test
    # Note: 1st parameter is normally named self
    def test_logout(self):
        # Checks that user have successful logout and doesn't display "Hello <Username>!" anymore
        r = requests.get(self.URL)
        # status code 200 means we got a response back, user have logged out
        self.assertEquals(r.status_code, 200)
        # once user logged out, goes back to the home page and display hello world
        self.assertEquals(r.text, "Hello World!")
        
    # Julia's Test
    def test_home(self):
        r = requests.get(self.URL'/groups')
        # status code 200 means we got a response back, user entered group
        self.assertEquals(r.status_code, 200)
        # if user isn't in any group, return "You aren't in any groups!"
        self.assertEquals(r.text, "You aren't in any groups!")
