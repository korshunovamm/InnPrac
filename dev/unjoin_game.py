import tornado.web

from domain.server.api.users.login.auth import get_user_info
from domain.mongoDB import GameMongo, UserMongo


class UnjoinGame(tornado.web.RequestHandler):
    def post(self):
        jwt_text = self.get_cookie("user")
        if jwt_text:
            status, user = get_user_info(jwt_text)
            if status:
                game_uuid = self.get_argument("ga_uuid")
                if game_uuid in user['games']:
                    ga = GameMongo.get_game(game_uuid)
                    if ga.get_status() == 'waiting':
                        del ga.labs[user['games'][game_uuid]]
                        GameMongo.update_game(ga)
                        UserMongo.remove_player_from_game(user["login"], game_uuid)
                        self.write({'status': 'ok', 'message': "Removed from game"})
                        self.set_status(200)
                    else:
                        self.write({'status': 'error', 'message': 'Game is already started or finished'})
                        self.set_status(400)
                else:
                    self.write({'status': 'error', 'message': 'User not in game'})
                    self.set_status(200)
            else:
                self.write({'status': 'error', 'message': 'Invalid token'})
                self.set_status(401)
        else:
            self.redirect("/login?redirect=" + self.request.path)
            self.set_status(401)
