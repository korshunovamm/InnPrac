from tornado.web import RequestHandler

from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo, UserMongo
from server.set_default_headers import set_default_headers


def delete_user_from_game(game, user_info):
    user_login = user_info["login"]
    user_game_login = user_info['games'][game.get_uuid()]
    if game.remove_lab(user_game_login):
        UserMongo.remove_player_from_game(user_login, game.get_uuid())
        GameMongo.update_game(game)
        return True
    else:
        return False


class DeleteUserFromGame(RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            if "ga_uuid" in self.request.query_arguments:
                user_info = get_user_info(jwt_text)
                if user_info[0]:
                    ga_uuid = self.request.query_arguments["ga_uuid"][0].decode('utf-8')
                    game = GameMongo.get_game(ga_uuid)
                    if not game:
                        self.write(dict(result="error", message="Game not found"))
                        return
                    if game.status != "waiting":
                        self.write(dict(result="error", message="Game already started"))
                        return
                    if user_info[1]["privilege"]:
                        if "us_login" in self.request.query_arguments:
                            cur_user_info = UserMongo.get_user(self.request.query_arguments["us_login"][0]
                                                               .decode('utf-8'))
                            if not cur_user_info:
                                self.write(dict(result="error", message="User not found"))
                                return
                            if not (game.get_uuid() in cur_user_info["games"]):
                                self.write(dict(result="error", message="User not in game"))
                                return
                            if delete_user_from_game(game, cur_user_info):
                                self.write(dict(result="ok", message="User deleted from game"))
                            else:
                                self.write(dict(result="error", message="User not found in game"))
                        else:
                            if delete_user_from_game(game, user_info):
                                self.write(dict(result="ok", message="User deleted from game"))
                            else:
                                self.write(dict(result="error", message="User not found in game"))
                    else:
                        if delete_user_from_game(game, user_info):
                            self.write(dict(result="ok", message="User deleted from game"))
                        else:
                            self.write(dict(result="error", message="User not found in game"))
                else:
                    self.clear_cookie("user")
                    self.redirect("/login")
            else:
                self.write(dict(result="error", message="Bad request"))
                self.set_status(400)
        else:
            self.redirect("/login?error=invalid_login")

    def set_default_headers(self):
        set_default_headers(self)
