def buy_logistic_service(websocket, data):
    if websocket.game.stage == 1:
        res = websocket.game.labs[websocket.pl_uuid].buy_logistic_service()
        if res:
            return {"result": "ok", "message": "", "data": websocket.game.labs[websocket.pl_uuid].services}
        return {"result": "error", "message": "You can't buy logistic service"}
    return {"result": "error", "message": "You can't buy logistic service"}

def buy_training_service(websocket, data):
    if websocket.game.stage == 1:
        res = websocket.game.labs[websocket.pl_uuid].buy_training_service()
        if res:
            return {"result": "ok", "message": "", "data": websocket.game.labs[websocket.pl_uuid].services}
        return {"result": "error", "message": "You can't buy training service"}
    return {"result": "error", "message": "You can't buy training service"}