import tornado.web

from game.game import Game
from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo


class NewGame(tornado.web.RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            userInfo = get_user_info(jwt_text)
            if userInfo[0]:
                if userInfo[1]["privilege"]:
                    game = Game()
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
            self.redirect("/login?error=invalid_login")

