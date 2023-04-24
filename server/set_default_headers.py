import tornado


def set_default_headers(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


def setup_default_headers():
    tornado.web.RequestHandler.set_default_headers = set_default_headers
    tornado.websocket.WebSocketHandler.set_default_headers = set_default_headers
