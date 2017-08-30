import app
import flask_testing
import requests
import unittest

class ServerIntegrationTest(flask_testing.LiveServerTestCase):
    def create_app(self):
        return app.app

    def test_index_length(self):
        response = requests.get(self.get_server_url())
        print len(response.text)
        self.assertNotEquals(len(response.text), 0)
        
    def test_response(self):
        response = requests.get(self.get_server_url())
        self.assertNotEquals(response, "<Response [200]>")

if __name__ == '__main__':
    unittest.main()