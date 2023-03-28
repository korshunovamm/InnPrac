def buy(websocket, data):
    if websocket.game is not None:
        game = websocket.game
        if (data["credit"].lower() == "true" or
            data["credit"].lower() == "false") and data["eq_type"] in ["pre_analytic", "reporting"] or\
                (data["eq_type"] in ["auto", "semi_manual", "hand"] and
                 data.get("eq_color") in ["yellow", "red", "green", "blue", "purple", "grey"]):
            res = game.buy_equipment(websocket.pl_uuid, data["eq_type"],
                                     data.get("eq_color"), data["credit"].lower() == "true")
            if res[0]:
                return {"result": "ok", "message": "Equipment bought", "data": res[1].generate_dict()}
            else:
                return {"result": "error", "message": "Equipment not bought"}
        else:
            return {"result": "error", "message": "Invalid data"}
    else:
        return {"result": "error", "message": "Game not found"}


def sell(websocket, data):
    if websocket.game is not None:
        game = websocket.game
        if game.sell_equipment(websocket.pl_uuid, data["eq_uuid"]):
            return {"result": "ok", "message": "Equipment sold"}
        else:
            return {"result": "error", "message": "Equipment not sold"}
    else:
        return {"result": "error", "message": "Game not found"}


def buy_lis(websocket, data):
    game = websocket.game
    res = game.buy_lis(websocket.pl_uuid, data["eq_uuid"])
    if res[0]:
        return {"result": "ok", "message": "LIS bought", "data": res[1].generate_dict()}
    else:
        return {"result": "error", "message": "LIS not bought"}


def buy_service_contract(websocket, data):
    game = websocket.game
    res = game.buy_service_contract(websocket.pl_uuid, data["eq_uuid"])
    if res[0]:
        return {"result": "ok", "message": "Service contract bought", "data": res[1].generate_dict()}
    else:
        return {"result": "error", "message": "Service contract not bought"}


def buy_service_maintenance(websocket, data):
    res = websocket.game.buy_service_maintenance(websocket.pl_uuid, data["eq_uuid"])
    if res[0]:
        return {"result": "ok", "message": "Service maintenance", "data": res[1].generate_dict()}
    else:
        return {"result": "error", "message": "Service maintenance not bought"}


def buy_reagents(websocket, data):
    if websocket.game.labs[websocket.pl_uuid].get_equipment(data["eq_uuid"]) is not None and isinstance(data["count"], int):
        res = websocket.game.buy_reagents(websocket.pl_uuid, data["eq_uuid"], data["count"])
        if res[0]:
            return {"result": "ok", "message": "Reagents bought", "data": res[1].generate_dict()}
        else:
            return {"result": "error", "message": "Reagents not bought"}
    else:
        return {"result": "error", "message": "Invalid data, dont found equipment or count is not int"}


def move_equipment_to_room(websocket, data):
    game = websocket.game
    if game.move_equipment_to_room(websocket.pl_uuid, data["ro_uuid"], data["eq_uuid"]):
        return {"result": "ok", "message": "Equipment moved"}
    else:
        return {"result": "error", "message": "Equipment not moved"}


def move_equipment_from_room(websocket, data):
    game = websocket.game
    if game.move_equipment_from_room(websocket.pl_uuid, data["ro_uuid"]):
        return {"result": "ok", "message": "Equipment moved"}
    else:
        return {"result": "error", "message": "Equipment not moved"}
