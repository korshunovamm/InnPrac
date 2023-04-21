import json
import os

from tornado.web import RequestHandler

from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo
from server.set_default_headers import set_default_headers


class GoToNextStage(RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            if "ga_uuid" in self.request.query_arguments:
                user_info = get_user_info(jwt_text)
                if user_info[0]:
                    if user_info[1]["privilege"]:
                        game = GameMongo.get_game(self.request.query_arguments["ga_uuid"][0].decode('utf-8'))
                        if not game:
                            self.write({"result": "error", "message": "Game not found"})
                            return
                        if game.status != "running":
                            self.write({"result": "error", "message": "Game not running"})
                            return
                        if game.stage == 1:
                            game.transition_to_stage_2()
                        else:
                            game.transition_to_stage_1()
                        if not os.path.exists("archive/"):
                            os.makedirs("archive/")
                        if not os.path.exists("archive/" + game.uuid):
                            os.makedirs("archive/" + game.uuid)
                        f = open("archive/" + game.get_uuid() + "/" + str(game.month) + "_" + str(game.stage) + ".json",
                                 "a")
                        f.write(json.dumps(game.generate_dict()))
                        f.close()
                        GameMongo.update_game(game)
                        self.write(dict(result="ok", message="Game updated"))
                    else:
                        self.write({"result": "error", "message": "Forbidden"})
                        self.set_status(403)
                else:
                    self.clear_cookie("user")
                    self.redirect("/login")
            else:
                self.write({"result": "error", "message": "Bad request"})
                self.set_status(400)
        else:
            self.redirect("/login?error=invalid_login")

    def set_default_headers(self):
        set_default_headers(self)