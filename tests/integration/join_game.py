import json
import tornado
import tornado.web
from tornado import testing
from domain.server.api.users.join_game import JoinGame


join_game_adr = "http://localhost:8888/login?redirect=/join_game/"

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader, Dumper


class TestAddressServiceApp(tornado.testing.AsyncHTTPTestCase):
    def get_app(self) -> tornado.web.Application:
        app = tornado.web.Application([(r"/join_game/.*", JoinGame)])
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

        # self.assertEqual(
        #     self.addr0,
        #     json.loads(r.body.decode('utf-8'))
        # )
        # # GET: error cases
        # r = self.fetch(
        #     ADDRESSBOOK_ENTRY_URI_FORMAT_STR.format(id='no-such-id'),
        #     method='GET',
        #     headers=None,
        # )
        # self.assertEqual(r.code, 404)
        # # Update that address
        # r = self.fetch(
        #     addr_uri,
        #     method='PUT',
        #     headers=self.headers,
        #     body=json.dumps(self.addr1),
        # )
        # self.assertEqual(r.code, 204)
        # r = self.fetch(
        #     addr_uri,
        #     method='GET',
        #     headers=None,
        # )
        # self.assertEqual(r.code, 200)
        # self.assertEqual(
        #     self.addr1,
        #     json.loads(r.body.decode('utf-8'))
        # )
        # # PUT: error cases
        # r = self.fetch(
        #     addr_uri,
        #     method='PUT',
        #     headers=self.headers,
        #     body='it is not json',
        # )
        # self.assertEqual(r.code, 400)
        # self.assertEqual(r.reason, 'Invalid JSON body')
        # r = self.fetch(
        #     ADDRESSBOOK_ENTRY_URI_FORMAT_STR.format(id='1234'),
        #     method='PUT',
        #     headers=self.headers,
        #     body=json.dumps(self.addr1),
        # )
        # self.assertEqual(r.code, 404)
        # # Delete that address
        # r = self.fetch(
        #     addr_uri,
        #     method='DELETE',
        #     headers=None,
        # )
        # self.assertEqual(r.code, 204)
        # r = self.fetch(
        #     addr_uri,
        #     method='GET',
        #     headers=None,
        # )
        # self.assertEqual(r.code, 404)
        # # DELETE: error cases
        # r = self.fetch(
        #     addr_uri,
        #     method='DELETE',
        #     headers=None,
        # )
        # self.assertEqual(r.code, 404)
        # # Get all addresses in the address book, must be ZERO
        # r = self.fetch(
        #     ADDRESSBOOK_ENTRY_URI_FORMAT_STR.format(id=''),
        #     method='GET',
        #     headers=None,
        # )
        # all_addrs = json.loads(r.body.decode('utf-8'))
        # self.assertEqual(r.code, 200, all_addrs)
        # self.assertEqual(len(all_addrs), 0, all_addrs)