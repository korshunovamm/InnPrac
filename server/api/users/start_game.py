from tornado.web import RequestHandler

from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo


class StartGame(RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            if "ga_uuid" in self.request.body_arguments:
                ga = GameMongo.get_game(self.get_body_argument("ga_uuid"))
                user_info = get_user_info(jwt_text)
                if user_info[0]:
                    if user_info[1]["privilege"]:
                        if ga:
                            if ga.get_status() == 'waiting':
                                ga.set_status("running")
                                GameMongo.update_game(ga)
                                self.write({"result": "ok", "message": "Started game"})
                                self.set_status(200)
                            else:
                                self.write({"result": "error", "message": "Game is already started or finished"})
                                self.set_status(400)
                        else:
                            self.write({"result": "error", "message": "Game not found"})
                            self.set_status(404)
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