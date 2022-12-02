import json

from tornado import websocket

from server.api.game.actions import player
from server.api.game.actions.entitys import room, equipment, tradeReq
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
        },
        "move_equipment_from_room": {
            "need_data": True,
            "action": equipment.move_equipment_from_room,
            "required_data": [{"name": "ro_uuid", "optional": False}]
        },
        "move_equipment_to_room": {
            "need_data": True,
            "action": equipment.move_equipment_to_room,
            "required_data": [{"name": "eq_uuid", "optional": False}, {"name": "ro_uuid", "optional": False}]
        },
        "buy_lis": {
            "need_data": True,
            "action": equipment.buy_lis,
            "required_data": [{"name": "eq_uuid", "optional": False}]
        },
        "buy_staff": {
            "need_data": True,
            "action": room.buy_staff,
            "required_data": [{"name": "ro_uuid", "optional": False}, {"name": "st_type", "optional": False},
                              {"name": "amount", "optional": False}]
        },
        "sell_staff": {
            "need_data": True,
            "action": room.sell_staff,
            "required_data": [{"name": "ro_uuid", "optional": False}, {"name": "st_type", "optional": False}]
        },
        "buy_logistic_service": {
            "need_data": False,
            "action": player.buy_logistic_service
        },
        "buy_training_service": {
            "need_data": False,
            "action": player.buy_training_service
        },
        "buy_service_contract": {
            "need_data": True,
            "action": equipment.buy_service_contract,
            "required_data": [{"name": "eq_uuid", "optional": False}]
        },
        "buy_service_maintenance": {
            "need_data": True,
            "action": equipment.buy_service_maintenance,
            "required_data": [{"name": "eq_uuid", "optional": False}]
        },
        "set_orders_input": {
            "need_data": True,
            "action": player.set_orders_input,
            "required_data": [{"name": "order_colors", "optional": False}]
        },
        "set_payment_type": {
            "need_data": True,
            "action": player.set_payment_type,
            "required_data": [{"name": "payment_type", "optional": False}]
        },
        "move_staff": {
            "need_data": True,
            "action": room.move_staff,
            "required_data": [{"name": "st_type", "optional": False}, {"name": "ro_from_uuid", "optional": False},
                              {"name": "ro_to_uuid", "optional": False}, {"name": "amount", "optional": False}]
        },
        "buy_ad": {
            "need_data": True,
            "action": player.buy_ad,
            "required_data": [{"name": "count", "optional": False}]
        },
        "change_lab_name": {
            "need_data": True,
            "action": player.set_lab_name,
            "required_data": [{"name": "new_lab_name", "optional": False}]
        },
        "buy_reagents": {
            "need_data": True,
            "action": equipment.buy_reagents,
            "required_data": [{"name": "eq_uuid", "optional": False}, {"name": "count", "optional": False}]
        },
        "new_trade_request": {
            "need_data": True,
            "action": tradeReq.new,
            "required_data": [{"name": "pl_1_uuid", "optional": False},
                              {"name": "pl_0_items", "optional": False}, {"name": "pl_1_items", "optional": False}]
        },
        "accept_trade_request": {
            "need_data": True,
            "action": tradeReq.accept,
            "required_data": [{"name": "tr_uuid", "optional": False}]
        },
    }

    def open(self):
        user_info = get_user_info(self.get_cookie('user'))
        if "ga_uuid" in self.request.query_arguments:
            if user_info[0]:
                if self.request.query_arguments["ga_uuid"][0].decode('utf-8') in user_info[1]["games"]:
                    uuid = self.request.query_arguments["ga_uuid"][0].decode("utf-8")
                    self.game = GameMongo.get_game(uuid)
                    if self.game.get_status() == "running":
                        if uuid not in connections:
                            connections[uuid] = []
                        connections[uuid].append(self)
                        self.pl_uuid = user_info[1]["games"][self.request.query_arguments["ga_uuid"][0].decode('utf-8')]
                        ret = dict(type="connect", data=dict(player_uuid=self.pl_uuid), game=self.game.generate_dict())
                        self.write_message(ret)
                    else:
                        self.close(4001, "game is not running")
                else:
                    self.close(4000, "You are not in this game")
            else:
                self.close(3000, "You are not logged in")
        else:
            self.close(1007, "Invalid request, you are not logged in")

    def on_message(self, message):
        try:
            msg_json = json.loads(message)
            if msg_json.get("type") == "action" and "action" in msg_json:
                if msg_json["action"] in self.actions:
                    if self.check_data(msg_json["action"], msg_json.get("data")):
                        msg_write = self.actions[msg_json["action"]]["action"](self, msg_json.get("data", None))
                        if msg_write['result'] == "ok":
                            GameMongo.update_game(self.game)
                            self.send_update(self.game.get_uuid(), self.pl_uuid)
                            msg_write['game'] = self.game.generate_dict()
                        self.write_message(msg_write)
                    else:
                        self.write_message({"type": "error", "message": "Not enough data"})
                else:
                    self.write_message({"type": "error", "message": "Invalid action"})
            else:
                self.write_message({"type": "error", "message": "Invalid message type"})
        except Exception as e:
            self.write_message({"type": "error", "error": str(e)})

    def on_close(self):
        if "game" in self.__dict__:  # if the game is not defined, the connection is not opened
            if self.game.get_uuid() in connections:
                connections[self.game.get_uuid()].remove(self)

    @staticmethod
    def check_data(action, data):
        if action in ConnectToGame.actions:
            if ConnectToGame.actions[action]["need_data"]:
                if data is not None:
                    for i in ConnectToGame.actions[action]["required_data"]:
                        if not i["optional"] and i["name"] not in data:
                            return False
                    return True
                return False
            return True
        return False

    @staticmethod
    def send_update(game_uuid, pl_uuid):
        if game_uuid in connections:
            game = GameMongo.get_game(game_uuid)
            for i in connections[game_uuid]:
                if i.pl_uuid != pl_uuid:
                    i.game = game
                    i.write_message({"type": "update", "game": GameMongo.get_game(game_uuid).generate_dict()})
