import unittest
import app

class ChatBotResponseTest(unittest.TestCase):
    def test_connect(self):
        response = app.connect()
        self.assertEquals(response, 'CONNECTED')
    def test_disconnect(self):
        response = app.disconnect()
        self.assertEquals(response, 'DISCONNECTED')
    def test_bot_about(self):
        response = app.botResponse("!! about")
        self.assertEquals(response, 'finished bot about')
    def test_bot_help(self):
        response = app.botResponse("!! help")
        self.assertEquals(response, 'finished bot help')
    def test_bot_say(self):
        response = app.botResponse("!! say")
        self.assertEquals(response, "finished bot say")
    def test_bot_name(self):
        response = app.botResponse("!! name")
        self.assertEquals(response, 'finished bot name')
    def test_bot_joke(self):
        response = app.botResponse("!! joke")
        self.assertEquals(response, 'finished bot joke')
    def test_bot_unrecognized(self):
        response = app.botResponse("!! test")
        self.assertEquals(response, 'finished bot unrecognized')
    def test_page_load(self):
        response = app.didPageLoad()
        self.assertEquals(response, 'PAGE LOADED')
    def test_reader(self):
        response = app.readerDone()
        self.assertEquals(response, 'READER DONE')

if __name__ == '__main__':
    unittest.main()