import tornado.web

from engine.game import Game
from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo


class NewGame(tornado.web.RequestHandler):
    def post(self):
        if "user" in self.request.cookies:
            jwt_text = self.get_cookie("user")
            if jwt_text:
                if "ga_name" in self.request.body_arguments:
                    user_info = get_user_info(jwt_text)
                    if user_info[0]:
                        if user_info[1]["privilege"]:
                            game = Game(str(self.request.body_arguments["ga_name"][0].decode('utf-8')))
                            GameMongo.add_game(game)
                            self.write({"result": "ok", "message": "Created game", "data": game.get_uuid()})
                            self.set_status(200)
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
        else:
            self.redirect("/login?error=not_logged_in")
