# from datetime import datetime
#
# from yaml import Loader, load
#
# import jwt
# data = load(open('configs/api.yaml'), Loader= Loader)
# encoded_jwt = jwt.encode({"some": "payload", "exp": str(int(round(datetime.now().timestamp())) + 2629743)}, data["jwt_secret"], algorithm="HS256", )
# try:
#     print(jwt.decode(encoded_jwt, data["jwt_secret"], algorithms=["HS256"]))
# except jwt.exceptions.InvalidSignatureError:
#     print("error")
# pass
import json

from game.game import Game

game = Game()
game.new_lab()
game_str = game
print(game_str)
