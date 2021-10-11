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