def buy(websocket, data):
    if websocket.game is not None:
        game = websocket.game
        if (data["credit"].lower() == "true" or data["credit"].lower() == "false") and (data["eq_type"] in ["pre_analytic", "reporting"] and "eq_color" not in data) or (data["eq_type"] in ["auto", "semi_manual", "hand"] and "eq_color" in data):
            res = game.buy_equipment(websocket.pl_uuid, data["eq_type"], data.get("eq_color"), data["credit"])
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