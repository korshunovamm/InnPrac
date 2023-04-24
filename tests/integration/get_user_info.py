import json
import tornado
import tornado.web
from tornado import testing
from domain.server.api.users.get_user_info import GetUserInfo


join_game_adr = "http://localhost:8888/login?redirect=/get_user_info"

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper


class TestAddressServiceApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self) -> tornado.web.Application:
        app = tornado.web.Application([(r"/get_user_info", GetUserInfo)])
        return app

    def test_get_query(self):
        r = self.fetch(
            join_game_adr.format(id=''),
            method='GET',
            headers=None,
        )
        body = r.body.decode("utf-8")
        self.assertEqual(r.code, 200)
        self.assertEqual(len(body), 38)

    def test_invalid_post_query(self):
        r = self.fetch(
            join_game_adr.format(id=''),
            method='POST',
            body='it is not json',
        )
        self.assertEqual(r.code, 400)

    def test_not_existing_adding(self):
        r = self.fetch(
            join_game_adr.format(id=''),
            method='POST',
            body=json.dumps({1: "error"}),
        )
        self.assertEqual(r.code, 400)
