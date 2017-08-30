import unittest
import app

class ChatBotResponseTest(unittest.TestCase):
    def test_fbtoken(self):
        client = app.socketio.test_client(app.app)
        client.emit('onfbtoken')
        r = client.get_received()
        self.assertEquals(r[0]['args'][0]['data'], 'fbtoken received')
    def test_fblogout(self):
        client = app.socketio.test_client(app.app)
        client.emit('onfblogout')
        r = client.get_received()
        self.assertEquals(r[0]['args'][0]['data'], 'fbtoken removed')
    def test_gtoken(self):
        client = app.socketio.test_client(app.app)
        client.emit('ongtoken')
        r = client.get_received()
        self.assertEquals(r[0]['args'][0]['data'], 'gtoken received')
    def test_glogout(self):
        client = app.socketio.test_client(app.app)
        client.emit('onglogout')
        r = client.get_received()
        self.assertEquals(r[0]['args'][0]['data'], 'gtoken removed')
    def test_botDone(self):
        client = app.socketio.test_client(app.app)
        client.emit('botDone')
        r = client.get_received()
        self.assertEquals(r[0]['args'][0]['data'], 'bot complete')

if __name__ == '__main__':
    unittest.main()