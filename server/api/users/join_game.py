import jwt
import tornado
from yaml import Loader, load

from server.mongoDB import UserMongo, GameMongo
from server.set_default_headers import set_default_headers


class JoinGame(tornado.web.RequestHandler):
    def get(self):
        jwt_str = self.get_cookie("user")
        if not jwt_str:
            self.redirect("/login?redirect=" + self.request.path)
        else:
            game_uuid = self.request.path.split("/")[2]
            config = load(open("configs/api.yaml"), Loader=Loader)
            try:
                user_info = jwt.decode(jwt_str, config["jwt_secret"], algorithms=["HS256"])
                game = GameMongo.get_game(game_uuid)
                if game:
                    if game.get_players_count() < game.get_max_players():
                        pl_uuid = game.new_lab(user_info["login"]).get_uuid()
                        res = UserMongo.add_player_to_game(user_info["login"], game_uuid, pl_uuid)
                        GameMongo.update_game(game)
                        if res[0]:
                            self.write({"status": "ok", "message": res[1]})
                        else:
                            self.write({"status": "error", "message": res[1]})
                    else:
                        self.write({"status": "error", "message": "Game is full"})
                        self.set_status(200)
                else:
                    self.write({"status": "error", "message": "Game does not exist"})
                    self.set_status(200)
            except jwt.exceptions.InvalidSignatureError:
                self.clear_cookie("user")
                self.redirect("/login?redirect=" + self.request.path + "&error=invalid_login")
            except jwt.exceptions.ExpiredSignatureError:
                self.clear_cookie("user")
                self.redirect("/login?redirect=" + self.request.path + "&expired=1")
        #  Check if the user is already in a game
        # if data['user'] in manage_game:
        #     return {'message': 'User already in game'}, 400
        # # Check if the game exists
        # if data['game'] not in manage_game:
        #     return {'message': 'Game does not exist'}, 400
        # # Check if the game is full
        # if len(manage_game[data['game']]) >= 2:
        #     return {'message': 'Game is full'}, 400
        # # Add the user to the game
        # manage_game[data['game']].append(data['user'])
        # return {'message': 'User joined game'}, 200

    def set_default_headers(self):
        set_default_headers(self)
