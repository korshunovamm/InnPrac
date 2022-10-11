def buy(websocket, data):
    if websocket.game is not None:
        game = websocket.game
        res = game.buy_room(websocket.pl_uuid)
        if res[0]:
            return {"result": "ok", "message": "Room bought", "data": res[1].generate_dict()}
        else:
            return {"result": "error", "message": "Room not bought"}
    else:
        return {"result": "error", "message": "Game not found"}


def sell(websocket, data):
    if websocket.game is not None:
        game = websocket.game
        if data["ro_uuid"] in game.labs[websocket.pl_uuid].rooms:
            res = game.sell_room(websocket.pl_uuid, data["ro_uuid"])
            if res:
                return {"result": "ok", "message": "Room sold"}
            else:
                return {"result": "error", "message": "Room not sold"}
        else:
            return {"result": "error", "message": "Room not found"}
    else:
        return {"result": "error", "message": "Game not found"}
