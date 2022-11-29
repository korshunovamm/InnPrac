def buy(websocket, data):
    game = websocket.game
    res = game.buy_room(websocket.pl_uuid)
    if res[0]:
        return {"result": "ok", "message": "Room bought", "data": res[1].generate_dict()}
    else:
        return {"result": "error", "message": "Room not bought"}


def sell(websocket, data):
    game = websocket.game
    if data["ro_uuid"] in game.labs[websocket.pl_uuid].rooms:
        res = game.sell_room(websocket.pl_uuid, data["ro_uuid"])
        if res:
            return {"result": "ok", "message": "Room sold"}
        else:
            return {"result": "error", "message": "Room not sold"}
    else:
        return {"result": "error", "message": "Room not found"}


def buy_staff(websocket, data):
    game = websocket.game
    if data["ro_uuid"] in game.labs[websocket.pl_uuid].rooms:
        if data["st_type"] in ["lab_assistant", "doctor"]:
            res = game.buy_staff(websocket.pl_uuid, data["ro_uuid"], data["st_type"], data["amount"])
            if res[0]:
                return {"result": "ok", "message": "Staff bought", "data": res[1].generate_dict()}
            else:
                return {"result": "error", "message": "Staff not bought"}
        else:
            return {"result": "error", "message": "Staff type not found"}
    else:
        return {"result": "error", "message": "Room not found"}


def sell_staff(websocket, data):
    game = websocket.game
    if data["ro_uuid"] in game.labs[websocket.pl_uuid].get_rooms():
        res = game.sell_staff(websocket.pl_uuid, data["ro_uuid"], data["st_type"])
        if res[0]:
            return {"result": "ok", "message": "Staff sold", "data": res[1].generate_dict()}
        else:
            return {"result": "error", "message": "Staff not sold"}
    else:
        return {"result": "error", "message": "Staff not found"}


def move_staff(websocket, data):
    if websocket.game.stage == 1:
        pl = websocket.game.labs[websocket.pl_uuid]
        if not data["st_type"] in ["doctor", "lab_assistant"]:
            return {"result": "error", "message": "Invalid data"}
        if not data["ro_from_uuid"] in pl.rooms\
                or not data["ro_to_uuid"] in pl.rooms:
            return {"result": "error", "message": "Invalid data"}
        ro_from = pl.rooms[data["ro_from_uuid"]]
        ro_to = pl.rooms[data["ro_to_uuid"]]
        if not isinstance(data["amount"], int):
            return {"result": "error", "message": "Invalid data"}
        if data["amount"] > ro_from.get_staff()[data["st_type"]]:
            return {"result": "error", "message": "Invalid data"}
        if data["amount"] > 4 - ro_to.get_staff()[data["st_type"]]:
            return {"result": "error", "message": "Invalid data"}
        for x in range(data["amount"]):
            pl.move_staff(data["ro_from_uuid"], data["ro_to_uuid"], data["st_type"])
        return {"result": "ok", "message": "Staff moved"}
