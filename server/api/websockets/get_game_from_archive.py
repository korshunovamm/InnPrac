import json
import os

from tornado.web import RequestHandler
from server.mongoDB import GameMongo


class GetGameFromArchive(RequestHandler):
    def get(self):
        global start_i
        start = self.get_argument("start", "1")
        end = self.get_argument("end", "1")
        ga_uuid = self.get_argument("ga_uuid", None)
        if start.isdigit() and end.isdigit():
            try:
                result = GameMongo.get_archive_game_of_period( start, end)
            except ValueError:
                self.write({"result": "error", "message": "Bad request"})
                self.set_status(400)
                return
            self.write({"result": "ok", "message": "Game archive", "data": str(result)})
            self.set_status(200)
        else:
            self.write(dict(result="error", message="Bad request"))
            self.set_status(400)
