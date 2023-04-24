import json
import tornado
import tornado.web
from tornado import testing
from domain.server.api.users.add_privilege import AddPrivilege


add_privilege_adr = "http://localhost:8888/add_privilege"

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper


class TestAddressServiceApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self) -> tornado.web.Application:
        app = tornado.web.Application([(r"/add_privilege", AddPrivilege)])
        return app

    def test_get_query(self):
        r = self.fetch(
            add_privilege_adr.format(id=''),
            method='GET',
            headers=None,
        )
        self.assertEqual(r.code, 405)

    def test_invalid_post_query(self):
        r = self.fetch(
            add_privilege_adr.format(id=''),
            method='POST',
            body='it is not json',
        )
        self.assertEqual(r.code, 403)

    def test_not_existing_adding(self):
        r = self.fetch(
            add_privilege_adr.format(id=''),
            method='POST',
            body=json.dumps({1: "error"}),
        )
        self.assertEqual(r.code, 400)
