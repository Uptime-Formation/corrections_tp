import flask_unittest
from src.monster_icon import app


class TestMainPage(flask_unittest.AppTestCase):

    def create_app(self):
        return app

    def test_mainpage(self, app):
        with app.test_client() as client:
            result = client.get('/')
            self.assertTrue(b'cannot connect to Redis' not in result.data)
            