import json

from tornado import websocket

from server.api.game.actions.entitys import room, equipment
from server.api.users.login.auth import get_user_info
from server.mongoDB import GameMongo

connections = {}


class ConnectToGame(websocket.WebSocketHandler):
    actions = {
        "buy_room": {
            "need_data": False,
            "action": room.buy
        },
        "sell_room": {
            "need_data": True,
            "action": room.sell,
            "required_data": [{"name": "ro_uuid", "optional": False}]
        },
        "buy_equipment": {
            "need_data": True,
            "action": equipment.buy,
            "required_data": [{"name": "eq_type", "optional": False}, {"name": "eq_color", "optional": True},
                              {"name": "credit", "optional": False}]
        },
        "sell_equipment": {
            "need_data": True,
            "action": equipment.sell,
            "required_data": [{"name": "eq_uuid", "optional": False}]
        }
    }

    def open(self):
        user_info = get_user_info(self.get_cookie('user'))
        if "game_uuid" in self.request.query_arguments:
            if user_info[0]:
                if self.request.query_arguments["game_uuid"][0].decode('utf-8') in user_info[1]["games"]:
                    uuid = self.request.query_arguments["game_uuid"][0].decode("utf-8")
                    if uuid not in connections:
                        connections[uuid] = []
                    connections[uuid].append(self)
                    self.game = GameMongo.get_game(uuid)
                    self.pl_uuid = user_info[1]["games"][self.request.query_arguments["game_uuid"][0].decode('utf-8')]
                    ret = dict(type="connect", data=dict(player_uuid=self.pl_uuid), game=self.game.generate_dict())
                    self.write_message(ret)
                else:
                    self.close(4000, "You are not in this game")
            else:
                self.close(3000, "You are not logged in")
        else:
            self.close(1007, "Invalid request, you are not logged in")

    def on_message(self, message):
        # try:
            msg_json = json.loads(message)
            if msg_json.get("type") == "action" and "action" in msg_json:
                if msg_json["action"] in self.actions:
                    if "data" in msg_json or self.check_data(msg_json["action"], msg_json.get("data")) or not \
                            self.actions[msg_json["action"]]["need_data"]:
                        msg_write = self.actions[msg_json["action"]]["action"](self, msg_json.get("data", None))
                        if msg_write['result'] == "ok":
                            GameMongo.update_game(self.game)
                            msg_write['game'] = self.game.generate_dict()
                        self.write_message(msg_write)
                    else:
                        self.write_message({"type": "error", "message": "Not enough data"})
                else:
                    self.write_message({"type": "error", "message": "Invalid action"})
            else:
                self.write_message({"type": "error", "message": "Invalid message type"})
        # except Exception as e:
        #     self.write_message({"type": "error", "error": str(e)})

    def on_close(self):
        print("WebSocket closed")

    @staticmethod
    def check_data(action, data):
        if action in ConnectToGame.actions:
            if ConnectToGame.actions[action]["need_data"]:
                for i in ConnectToGame.actions[action]["required_data"]:
                    if not i["optional"] and i["name"] not in data:
                        return False
                return True
            else:
                return True
        else:
            return False
